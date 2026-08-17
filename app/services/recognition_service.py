from app.repositories.face_embedding_repository import (
    get_all_face_embeddings,
)

from app.repositories.employee_repository import (
    find_by_employee_id,
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

    # Get employee details
    employee = find_by_employee_id(
        db=db,
        employee_id=best_match.employee_id,
    )

    if not employee:
        return None

    return {
        "employee_id": employee.id,
        "employee_code": employee.employee_code,
        "employee_name": employee.name,
        "similarity": best_score,
    }