from datetime import (
    datetime,
    timedelta,
    timezone,
)

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.ai.gemini_chat_service import (
    generate_general_answer,
    generate_grounded_answer,
)

from app.ai.portfolio_retriever import (
    retrieve_portfolio_context,
)
from app.core.config import settings
from app.models.chat_interaction import (
    ChatInteraction,
)


INSUFFICIENT_INFORMATION_ANSWER = (
    "I do not have enough portfolio information "
    "to answer that."
)

PORTFOLIO_KEYWORDS = {
    "bajirao",
    "salunke",
    "your portfolio",
    "his portfolio",
    "your profile",
    "his profile",
    "your resume",
    "his resume",
    "your project",
    "his project",
    "projects",
    "skills",
    "experience",
    "education",
    "research",
    "iit guwahati",
    "gate",
    "leetcode",
    "github",
    "linkedin",
    "recruitai",
    "hindi nlp",
    "assistant professor",
    "suitable for",
    "hire",
    "candidate",
}

GENERAL_KEYWORDS = {
    "explain",
    "what is",
    "how to",
    "write code",
    "program",
    "python",
    "java",
    "c++",
    "javascript",
    "react",
    "fastapi",
    "sql",
    "database",
    "machine learning",
    "deep learning",
    "algorithm",
    "data structure",
    "interview",
    "difference between",
    "example",
}


def detect_chat_mode(
    question: str,
) -> str:
    clean_question = question.lower()

    has_portfolio_signal = any(
        keyword in clean_question
        for keyword in PORTFOLIO_KEYWORDS
    )

    has_general_signal = any(
        keyword in clean_question
        for keyword in GENERAL_KEYWORDS
    )

    if has_portfolio_signal and has_general_signal:
        return "mixed"

    if has_portfolio_signal:
        return "portfolio"

    return "general"

class ChatRateLimitError(Exception):
    pass


def enforce_chat_rate_limit(
    database_session: Session,
    visitor_key: str,
) -> None:
    period_start = datetime.now(
        timezone.utc
    ) - timedelta(
        minutes=(
            settings.chat_rate_window_minutes
        )
    )

    recent_count = database_session.scalar(
        select(func.count())
        .select_from(ChatInteraction)
        .where(
            ChatInteraction.visitor_key
            == visitor_key,
            ChatInteraction.created_at
            >= period_start,
        )
    )

    if (
        int(recent_count or 0)
        >= settings.chat_rate_limit
    ):
        raise ChatRateLimitError(
            "Chat request limit reached. "
            "Please try again later."
        )


def save_chat_interaction(
    database_session: Session,
    visitor_key: str,
    question: str,
    answer: str,
    sources: list[dict],
    confidence_score: float,
    grounded: bool,
    model_name: str,
    retrieval_method: str,
) -> ChatInteraction:
    public_sources = [
        {
            key: value
            for key, value in source.items()
            if key != "content"
        }
        for source in sources
    ]

    interaction = ChatInteraction(
        visitor_key=visitor_key,
        question=question,
        answer=answer,
        source_refs=public_sources,
        confidence_score=confidence_score,
        grounded=grounded,
        model_name=model_name,
        retrieval_method=retrieval_method,
    )

    database_session.add(interaction)
    database_session.commit()
    database_session.refresh(interaction)

    return interaction


def answer_portfolio_question(
    database_session: Session,
    visitor_key: str,
    question: str,
    history: list[dict],
    top_k: int | None,
) -> dict:
    enforce_chat_rate_limit(
        database_session=database_session,
        visitor_key=visitor_key,
    )

    chat_mode = detect_chat_mode(
        question
    )

    if chat_mode == "general":
        answer = generate_general_answer(
            question=question,
            history=history,
        )

        interaction = save_chat_interaction(
            database_session=database_session,
            visitor_key=visitor_key,
            question=question,
            answer=answer,
            sources=[],
            confidence_score=0.0,
            grounded=False,
            model_name=settings.gemini_model_name,
            retrieval_method="general-gemini",
        )

        return {
            "interaction_id": interaction.id,
            "answer": answer,
            "grounded": False,
            "confidence_score": 0.0,
            "sources": [],
            "model_name": settings.gemini_model_name,
            "retrieval_method": "general-gemini",
            "answer_mode": "general",
        }

    (
        sources,
        retrieval_method,
        confidence_score,
    ) = retrieve_portfolio_context(
        database_session=database_session,
        question=question,
        top_k=top_k,
    )

    if not sources:
        if chat_mode == "mixed":
            answer = generate_general_answer(
                question=question,
                history=history,
            )

            interaction = save_chat_interaction(
                database_session=database_session,
                visitor_key=visitor_key,
                question=question,
                answer=answer,
                sources=[],
                confidence_score=0.0,
                grounded=False,
                model_name=settings.gemini_model_name,
                retrieval_method="mixed-general-fallback",
            )

            return {
                "interaction_id": interaction.id,
                "answer": answer,
                "grounded": False,
                "confidence_score": 0.0,
                "sources": [],
                "model_name": settings.gemini_model_name,
                "retrieval_method": "mixed-general-fallback",
                "answer_mode": "mixed",
            }

        interaction = save_chat_interaction(
            database_session=database_session,
            visitor_key=visitor_key,
            question=question,
            answer=(
                INSUFFICIENT_INFORMATION_ANSWER
            ),
            sources=[],
            confidence_score=0.0,
            grounded=False,
            model_name="retrieval-only",
            retrieval_method=retrieval_method,
        )

        return {
            "interaction_id": interaction.id,
            "answer": interaction.answer,
            "grounded": False,
            "confidence_score": 0.0,
            "sources": [],
            "model_name": interaction.model_name,
            "retrieval_method": (
                interaction.retrieval_method
            ),
            "answer_mode": "portfolio",
        }

    answer = generate_grounded_answer(
        question=question,
        history=history,
        sources=sources,
    )

    interaction = save_chat_interaction(
        database_session=database_session,
        visitor_key=visitor_key,
        question=question,
        answer=answer,
        sources=sources,
        confidence_score=confidence_score,
        grounded=True,
        model_name=settings.gemini_model_name,
        retrieval_method=retrieval_method,
    )

    public_sources = [
        {
            key: value
            for key, value in source.items()
            if key != "content"
        }
        for source in sources
    ]

    return {
        "interaction_id": interaction.id,
        "answer": answer,
        "grounded": True,
        "confidence_score": confidence_score,
        "sources": public_sources,
        "model_name": settings.gemini_model_name,
        "retrieval_method": retrieval_method,
        "answer_mode": chat_mode,
    }

def list_chat_interactions(
    database_session: Session,
    limit: int,
    offset: int,
) -> list[ChatInteraction]:
    statement = (
        select(ChatInteraction)
        .order_by(
            ChatInteraction.created_at.desc()
        )
        .limit(limit)
        .offset(offset)
    )

    return list(
        database_session.scalars(
            statement
        ).all()
    )


def get_chat_interaction_by_id(
    database_session: Session,
    interaction_id: int,
) -> ChatInteraction | None:
    return database_session.get(
        ChatInteraction,
        interaction_id,
    )


def delete_chat_interaction(
    database_session: Session,
    interaction: ChatInteraction,
) -> None:
    database_session.delete(interaction)
    database_session.commit()