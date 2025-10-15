# 🧠 SmartShift-AI

**SmartShift-AI** is an AI-powered **Shift-End Reporting and Meeting Summarization System** built with **Python, FastAPI, Whisper**, and **NLP**.  
It transcribes meeting recordings, generates structured summaries, and stores reports for later retrieval.

---

## 🚀 Features

- Speech-to-Text (OpenAI Whisper)  
- NLP-based summarization (Hugging Face Transformers)  
- Stores meeting metadata (title, date/time)  
- Persistent storage with SQLite via SQLAlchemy  
- REST API built with FastAPI  
- Future: Flutter dashboard for viewing reports

---

## 🧱 Project Structure

SmartShift-AI/
|
|-- backend/
|   |-- api/
|   |   |-- models/
|   |   |   └── schemas.py              # Pydantic API models (request/response)
|   |   |
|   |   |-- routes/
|   |   |   └── transcription.py        # All endpoints (transcribe, reports, summarize)
|   |   |
|   |   └── crud.py                     # Database interaction functions
|   |
|   |-- database/
|   |   |-- db.py                       # Database connection (SQLAlchemy + SQLite)
|   |   └── models.py                   # SQLAlchemy models for DB tables
|   |
|   |-- utils/
|   |   └── summarizer.py               # NLP summarizer (Hugging Face - BART)
|   |
|   |-- main.py                         # FastAPI app entry point
|   └── requirements.txt                # Python dependencies
|
|-- .gitignore                          # Ignore build, venv, cache files
└── README.md                           # Project documentation (this file)

---

## 🧰 Tech Stack

- **Backend:** FastAPI (Python)  
- **Speech Recognition:** OpenAI Whisper  
- **NLP Summarization:** Hugging Face Transformers (facebook/bart-large-cnn)  
- **Database:** SQLite (SQLAlchemy)  
- **Language:** Python 3.11  
- **Frontend (planned):** Flutter

---

## ⚙️ Installation & Setup (complete)

Follow these exact steps. Commands are for **Windows PowerShell** unless noted.

1) Clone repository
    git clone https://github.com/Akhilesh-Ankur09/SmartShift-AI.git
    cd SmartShift-AI

2) Create & activate virtual environment (Windows PowerShell)
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    # If PowerShell prevents execution, run once (as Administrator or with permission):
    # Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

   (For Command Prompt)
    .venv\Scripts\activate.bat

   (For macOS / Linux)
    python3 -m venv .venv
    source .venv/bin/activate

3) Install backend dependencies
    cd backend
    python -m pip install --upgrade pip
    pip install -r requirements.txt

   If `torch` install fails, install CPU wheel first (example):
    pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
    pip install openai-whisper

4) Run the FastAPI server (development)
    uvicorn main:app --reload

   Open the API docs:
    http://127.0.0.1:8000/docs

---

## 🔌 API Endpoints

- `POST /api/transcribe`  
  Upload an audio (.wav/.mp4) file with optional form field `meeting_title`. Transcribes, saves transcript & metadata to DB, returns preview and `meeting_id`.

- `GET /api/reports`  
  Returns a list of saved meeting reports (id, title, date, etc).

- `POST /api/summarize/{meeting_id}`  
  Generates (or regenerates) an NLP summary for a stored meeting and saves it in DB.

---

## 💾 Database schema (MeetingReport table)

- `id` (Integer, PK)  
- `meeting_title` (String)  
- `meeting_date` (DateTime)  
- `started_at` (DateTime)  
- `ended_at` (DateTime, optional)  
- `transcript_text` (Text)  
- `final_summary` (Text, optional)  
- `raw_transcript_path` (String, optional)

---

## 🧪 Example usage (curl)

Upload and transcribe:
    curl -X POST "http://127.0.0.1:8000/api/transcribe" \
      -F "file=@/path/to/meeting.wav" \
      -F "meeting_title=Daily Sync"

List reports:
    curl http://127.0.0.1:8000/api/reports

Summarize a stored meeting:
    curl -X POST http://127.0.0.1:8000/api/summarize/1

---

## 🧭 Development Commands

- Start server (dev): `uvicorn main:app --reload`  
- Run on all interfaces (prod-like): `uvicorn main:app --host 0.0.0.0 --port 8000`  
- Freeze dependencies: `pip freeze > requirements.txt`

---

## 📈 Roadmap

- [x] FastAPI + Whisper transcription  
- [x] SQLite database persistence (SQLAlchemy)  
- [x] NLP summarization (Hugging Face BART)  
- [ ] Interval-based (periodic) summaries during long meetings  
- [ ] Flutter frontend dashboard (view/export reports)  
- [ ] Dockerfile + Deploy (Render / Railway / VPS)  
- [ ] Authentication & permissions  
- [ ] Export to PDF/email

---

## 🧑‍💻 Author

**Akhilesh Ankur**  
MCA Graduate • AI & Automation Enthusiast  
GitHub: https://github.com/Akhilesh-Ankur09  
LinkedIn: https://www.linkedin.com/in/akhilesh-ankur-3354712aa

---

## 🪪 License

This project is available under the **MIT License**. See `LICENSE` file.

---

## 🤝 Contributing

Contributions, issues and feature requests are welcome — please open issues or PRs on GitHub.

