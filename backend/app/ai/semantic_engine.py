from threading import Lock

import numpy as np
from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)
from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from app.core.config import settings


_embedding_model = None
_model_loading_failed = False
_model_lock = Lock()


def get_embedding_model():
    global _embedding_model
    global _model_loading_failed

    if _embedding_model is not None:
        return _embedding_model

    if _model_loading_failed:
        return None

    with _model_lock:
        if _embedding_model is not None:
            return _embedding_model

        if _model_loading_failed:
            return None

        try:
            from sentence_transformers import (
                SentenceTransformer,
            )

            _embedding_model = SentenceTransformer(
                settings.embedding_model_name
            )

            return _embedding_model

        except Exception:
            _model_loading_failed = True
            return None


def calculate_tfidf_similarity(
    query: str,
    documents: list[str],
) -> list[float]:
    if not documents:
        return []

    try:
        vectorizer = TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2),
            max_features=15000,
        )

        matrix = vectorizer.fit_transform(
            [query, *documents]
        )

        scores = cosine_similarity(
            matrix[0:1],
            matrix[1:],
        )[0]

        return [
            float(
                max(
                    0.0,
                    min(1.0, score),
                )
            )
            for score in scores
        ]

    except ValueError:
        return [
            0.0
            for _ in documents
        ]


def calculate_semantic_similarity(
    query: str,
    documents: list[str],
) -> tuple[list[float], str]:
    if not documents:
        return [], "no-evidence"

    embedding_model = get_embedding_model()

    if embedding_model is not None:
        try:
            embeddings = embedding_model.encode(
                [query, *documents],
                batch_size=16,
                convert_to_numpy=True,
                normalize_embeddings=True,
                show_progress_bar=False,
            )

            query_embedding = embeddings[0]
            document_embeddings = embeddings[1:]

            scores = np.dot(
                document_embeddings,
                query_embedding,
            )

            normalized_scores = [
                float(
                    max(
                        0.0,
                        min(1.0, score),
                    )
                )
                for score in scores
            ]

            return (
                normalized_scores,
                settings.embedding_model_name,
            )

        except Exception:
            pass

    return (
        calculate_tfidf_similarity(
            query,
            documents,
        ),
        "tfidf-fallback",
    )