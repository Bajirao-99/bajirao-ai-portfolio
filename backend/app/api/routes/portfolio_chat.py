from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.orm import Session

from app.ai.gemini_chat_service import (
    GeminiChatError,
)
from app.api.dependencies.auth import (
    get_current_admin,
)
from app.db.database import get_db
from app.models.admin_user import AdminUser
from app.schemas.portfolio_chat import (
    ChatInteractionHistoryResponse,
    PortfolioChatRequest,
    PortfolioChatResponse,
)
from app.services.portfolio_chat_service import (
    ChatRateLimitError,
    answer_portfolio_question,
    delete_chat_interaction,
    get_chat_interaction_by_id,
    list_chat_interactions,
)


public_router = APIRouter(
    prefix="/api/v1/ai/chat",
    tags=["AI Portfolio Chatbot"],
)


admin_router = APIRouter(
    prefix="/api/v1/admin/chat-interactions",
    tags=["Admin Chat Interactions"],
)


@public_router.get(
    "/suggestions",
    response_model=list[str],
)
def chatbot_suggestions():
    return [
        "What are Bajirao's strongest technical skills?",
        "Explain the RecruitAI Pro project.",
        "Is he suitable for a Python backend role?",
        "Explain FastAPI in simple words.",
        "Give me Python interview questions.",
        "What is RAG in AI?",
        "Explain REST API with example.",
        "How should I prepare for an AI/ML interview?",
    ]

@public_router.post(
    "",
    response_model=PortfolioChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def ask_portfolio_chatbot(
    request_data: PortfolioChatRequest,
    database_session: Session = Depends(get_db),
):
    try:
        return answer_portfolio_question(
            database_session=database_session,
            visitor_key=str(
                request_data.visitor_key
            ),
            question=request_data.question.strip(),
            history=[
                message.model_dump()
                for message
                in request_data.history
            ],
            top_k=request_data.top_k,
        )

    except ChatRateLimitError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_429_TOO_MANY_REQUESTS
            ),
            detail=str(error),
        ) from error

    except GeminiChatError as error:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=str(error),
        ) from error


@admin_router.get(
    "",
    response_model=list[
        ChatInteractionHistoryResponse
    ],
)
def read_chat_interactions(
    limit: int = Query(
        default=50,
        ge=1,
        le=200,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    return list_chat_interactions(
        database_session=database_session,
        limit=limit,
        offset=offset,
    )


@admin_router.delete(
    "/{interaction_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def remove_chat_interaction(
    interaction_id: int,
    database_session: Session = Depends(get_db),
    _current_admin: AdminUser = Depends(
        get_current_admin
    ),
):
    interaction = get_chat_interaction_by_id(
        database_session=database_session,
        interaction_id=interaction_id,
    )

    if interaction is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Chat interaction not found.",
        )

    delete_chat_interaction(
        database_session=database_session,
        interaction=interaction,
    )

    return Response(
        status_code=status.HTTP_204_NO_CONTENT
    )