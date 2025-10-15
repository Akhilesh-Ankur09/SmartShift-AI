# 🧠 SmartShift-AI

**SmartShift-AI** is an AI-powered **Shift-End Reporting and Meeting Summarization System** built with **Python, FastAPI, Whisper**, and **NLP**.  
It automatically transcribes meeting recordings, generates structured summaries, and stores all reports for future access — making your workflow faster, smarter, and organized.

---

## 🚀 Features

- 🎙 **Speech-to-Text (OpenAI Whisper)** — Accurately transcribes meeting audio into text.  
- 🧾 **Automatic Report Generation** — NLP-based summarization of meeting discussions.  
- 🕒 **Meeting Metadata** — Each report stores date, title, transcript, and summaries.  
- 🗃 **Persistent Storage (SQLite)** — Saves meeting records for retrieval anytime.  
- ⚙️ **REST API with FastAPI** — Easy-to-use, interactive endpoints.  
- 📱 **Future Integration** — Flutter frontend for dashboards and shift-end summaries.

---

## 🧱 Project Structure

SmartShift-AI/
│
├── backend/
│ ├── api/
│ │ ├── models/
│ │ │ └── schemas.py # Pydantic API models (request/response)
│ │ ├── routes/
│ │ │ └── transcription.py # All endpoints (transcribe, reports, summarize)
│ │ └── crud.py # Database interaction functions
│ │
│ ├── database/
│ │ ├── db.py # Database connection (SQLAlchemy + SQLite)
│ │ └── models.py # SQLAlchemy models for DB tables
│ │
│ ├── utils/
│ │ └── summarizer.py # NLP summarizer (Hugging Face - BART)
│ │
│ ├── main.py # FastAPI app entry point
│ └── requirements.txt # Python dependencies
│
├── .gitignore # Ignore build, venv, cache files
└── README.md # Project documentation (this file)


---

## 🧰 Tech Stack

| Component | Technology |
|------------|-------------|
| **Backend** | FastAPI (Python) |
| **Speech Recognition** | OpenAI Whisper |
| **NLP Summarization** | Hugging Face Transformers (BART) |
| **Database** | SQLite (via SQLAlchemy ORM) |
| **Language** | Python 3.11 |
| **Frontend (Planned)** | Flutter |

---

## ⚙️ Installation & Setup (Step-by-Step)

> 🧑‍💻 Follow these steps carefully to set up your environment.

### 🪜 1. Clone the Repository
```bash
git clone https://github.com/Akhilesh-Ankur09/SmartShift-AI.git
cd SmartShift-AI

🪜 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate   # For Windows
# OR
source .venv/bin/activate  # For Linux/Mac

🪜 3. Install Dependencies
```bash
cd backend
pip install -r requirements.txt

🪜 4. Run the FastAPI Server
```bash
uvicorn main:app --reload

✅ Server will start at:
👉 http://127.0.0.1:8000

✅ Interactive API Docs:
👉 http://127.0.0.1:8000/docs

🪜 5. Verify Setup
You should see logs like:

INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000


Then, open /docs to test your endpoints.

🧩 API Endpoints
Endpoint	Method	Description
/api/transcribe	POST	Upload an audio/video file, transcribe with Whisper, and save to DB
/api/reports	GET	Retrieve all saved meeting reports
/api/summarize/{meeting_id}	POST	Generate a summary for a specific meeting by ID

🧠 Example Workflow

1️⃣ Upload a meeting recording

POST /api/transcribe


Upload .wav or .mp4 file

(Optional) Add a meeting title
✅ Returns transcript preview and saves it to the database.

2️⃣ List all reports

GET /api/reports


Shows all saved meetings with title, date, and transcript IDs.

3️⃣ Generate a summary

POST /api/summarize/{meeting_id}


Replace {meeting_id} with the ID from /api/reports
✅ Returns and saves the NLP-generated summary.

🗂 Database Schema (MeetingReport Table)
Column	Type	Description
id	Integer (PK)	Unique report ID
meeting_title	String	Meeting name/title
meeting_date	DateTime	Date of meeting
started_at	DateTime	Meeting start time
ended_at	DateTime	Meeting end time
transcript_text	Text	Full meeting transcript
final_summary	Text	NLP-generated summary
raw_transcript_path	String	Path to raw audio file (optional)
🧱 Example JSON Responses
📩 /api/transcribe
{
  "message": "Transcription saved successfully!",
  "meeting_id": 1,
  "meeting_title": "Daily Standup",
  "meeting_date": "2025-10-12T12:32:15.321Z",
  "transcript_preview": "Today the team discussed progress..."
}

📤 /api/reports
[
  {
    "id": 1,
    "meeting_title": "Daily Standup",
    "meeting_date": "2025-10-12T12:32:15.321Z",
    "final_summary": null
  }
]

🧾 /api/summarize/1
{
  "meeting_id": 1,
  "meeting_title": "Daily Standup",
  "summary": "The team reviewed ongoing tasks, discussed blockers, and planned next steps."
}

🧭 Development Commands
Task	Command
Start server	uvicorn main:app --reload
Install deps	pip install -r requirements.txt
Freeze deps	pip freeze > requirements.txt
Run in prod (optional)	uvicorn main:app --host 0.0.0.0 --port 8080
📈 Roadmap

 FastAPI + Whisper integration

 SQLite database with SQLAlchemy ORM

 NLP summarization (BART model)

 Interval-based meeting summaries

 Flutter dashboard integration

 Docker & Render deployment

 User authentication system

 Export reports to PDF/Email

🧑‍💻 Author

Akhilesh Ankur
🎓 MCA Graduate | AI & Automation Enthusiast
📍 India
🔗 LinkedIn

💻 GitHub

🪪 License

This project is licensed under the MIT License — see the LICENSE
 file for details.

🤝 Contributing

Contributions are welcome!
Feel free to fork this repo, open issues, or create pull requests.

1. Fork the project
2. Create your feature branch (git checkout -b feature-name)
3. Commit your changes (git commit -m "Add feature-name")
4. Push to your branch (git push origin feature-name)
5. Open a Pull Request 🚀

🌟 Acknowledgements

[OpenAI Whisper](https://github.com/openai/whisper)
 for robust speech recognition

[Hugging Face Transformers](https://huggingface.co/transformers/)
 for text summarization

[FastAPI](https://fastapi.tiangolo.com/)
 for modern Python APIs

[SQLite](https://sqlite.org/)
 for easy local data storage