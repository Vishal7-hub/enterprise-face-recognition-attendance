# AI Face Recognition Attendance System

An AI-powered real-time attendance system that automatically recognizes registered employees through a webcam and marks attendance using facial recognition.

## Features

- Real-time webcam-based face recognition
- Automatic employee identification
- Face embeddings using InsightFace
- Cosine similarity-based face matching
- Automatic attendance marking
- Duplicate attendance prevention
- Unknown face detection
- Attendance history
- FastAPI REST APIs
- SQLite database
- Web-based dashboard

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- InsightFace
- ONNX Runtime
- SQLite
- HTML, CSS, JavaScript
- Uvicorn
- Git & GitHub
- Pytest

## Workflow

Employee Enrollment → Face Embedding Generation → Store Embedding → Live Webcam → Capture Frame → FastAPI → Face Recognition → Similarity Matching → Employee Identified → Attendance Automatically Marked

## Recognition

The system generates facial embeddings using InsightFace and compares the live camera embedding with stored employee embeddings using cosine similarity.

Recognition Threshold: 0.5

If the similarity score is below the threshold, the person is treated as an unknown employee.

## Main APIs

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /employees | Create employee |
| POST | /employees/{employee_code}/image | Enroll employee face |
| POST | /recognition/verify | Verify uploaded face |
| POST | /recognition/camera | Live recognition and automatic attendance |
| POST | /attendance/mark/{employee_id} | Mark attendance |
| GET | /attendance/employee/{employee_id} | Employee attendance history |
| GET | /attendance/date/{attendance_date} | Date-wise attendance |

## Project Structure
```text
app/
├── api/
├── core/
├── db/
├── models/
├── repositories/
├── schemas/
└── services/

frontend/
├── css/
├── js/
└── index.html

tests/
requirements.txt
.env.example
README.md

```



## Setup

git clone <https://github.com/Vishal7-hub/enterprise-face-recognition-attendance.git>

cd enterprise-face-recognition-attendance

python -m venv .venv

.venv\Scripts\activate

pip install -r requirements.txt

uvicorn app.main:app --reload

## Application

http://127.0.0.1:8000

## API Documentation

Swagger UI: http://127.0.0.1:8000/docs

## Future Improvements

- Liveness and anti-spoofing detection
- Multiple face recognition
- PostgreSQL / cloud database integration
- Authentication and admin dashboard
- Attendance analytics and reporting
- Dockerization and cloud deployment

## Author

**Vishal Kumar Roy**

B.Tech — Computer Science & Engineering (AI/ML)