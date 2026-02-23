AI Notes Summarizer

A full-stack AI web application that automatically summarizes user notes using Natural Language Processing (NLP).

##  Features
- AI text summarization (extractive NLP)
- Create, edit, delete notes
- Search and filter notes
- PostgreSQL database storage
- FastAPI backend
- Modern responsive UI
- REST API architecture

##  AI Approach
The system uses extractive summarization:
- Sentence tokenization (NLTK)
- Stopword removal
- Word frequency scoring
- Sentence ranking
- Top-sentence selection

##  Tech Stack
Frontend: HTML, CSS, JavaScript  
Backend: FastAPI (Python)  
Database: PostgreSQL  
AI/NLP: NLTK  

##  Project Structure

client/ → frontend
server/ → backend + AI


##  Setup Instructions

```bash
git clone <repo>
cd ai_notes_app
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python -m nltk.downloader punkt punkt_tab stopwords
uvicorn server.main:app --reload

Open:
http://127.0.0.1:8000/app

Future Enhancements

Summary length control

Generative AI summarization

Export notes

User accounts