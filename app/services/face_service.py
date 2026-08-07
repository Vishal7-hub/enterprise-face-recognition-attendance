import cv2
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

    embedding = faces[0].embedding

    return embedding