import cv2
import numpy as np

from insightface.app import FaceAnalysis

face_app = FaceAnalysis(
    name="buffalo_l"
)

face_app.prepare(
    ctx_id=-1
)


def generate_embedding(image_path: str):

    image = cv2.imread(image_path)

    if image is None:
        raise ValueError("Unable to read image")

    faces = face_app.get(image)

    if not faces:
        raise ValueError("No face detected")

    if len(faces) > 1:
        raise ValueError("Multiple faces detected")

    return faces[0].embedding


def embedding_from_bytes(embedding_bytes: bytes):

    return np.frombuffer(
        embedding_bytes,
        dtype=np.float32,
    )


def cosine_similarity(
    embedding1: np.ndarray,
    embedding2: np.ndarray,
):
    embedding1 = embedding1 / np.linalg.norm(embedding1)
    embedding2 = embedding2 / np.linalg.norm(embedding2)

    return float(
        np.dot(embedding1, embedding2)
    )