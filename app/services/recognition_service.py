from pathlib import Path

from app.repositories.face_embedding_repository import (
    get_all_face_embeddings,
)
from app.services.face_service import (
    generate_embedding,
    embedding_from_bytes,
    cosine_similarity,
)


MATCH_THRESHOLD = 0.5


def recognize_face(
    db,
    image_path: str,
):
    query_embedding = generate_embedding(image_path)

    stored_embeddings = get_all_face_embeddings(db)

    if not stored_embeddings:
        return None

    best_match = None
    best_score = -1.0

    for record in stored_embeddings:

        stored_embedding = embedding_from_bytes(
            record.embedding
        )

        score = cosine_similarity(
            query_embedding,
            stored_embedding,
        )

        if score > best_score:
            best_score = score
            best_match = record

    if best_score < MATCH_THRESHOLD:
        return None

    return {
        "employee_id": best_match.employee_id,
        "similarity": best_score,
    }