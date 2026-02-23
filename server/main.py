from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.db import get_connection
from pydantic import BaseModel
from server.ai.summarizer import summarize_text
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

# ✅ CORS must be immediately after app creation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class NoteCreate(BaseModel):
    content: str

@app.get("/")
def read_root():
    return {"message": "AI Notes Summarizer API running"}

@app.get("/test-db")
def test_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT version();")
    version = cur.fetchone()
    cur.close()
    conn.close()
    return {"postgres_version": version}

@app.post("/notes")
def create_note(note: NoteCreate):
    # ✅ Generate AI summary
    summary = summarize_text(note.content)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO notes (content, summary) VALUES (%s, %s) RETURNING id;",
        (note.content, summary)
    )
    note_id = cur.fetchone()[0]

    conn.commit()
    cur.close()
    conn.close()

    return {
        "message": "Note created",
        "id": note_id,
        "summary": summary
    }

@app.get("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, content, summary, created_at FROM notes ORDER BY created_at DESC;"
    )
    rows = cur.fetchall()

    cur.close()
    conn.close()

    notes = []
    for r in rows:
        notes.append({
            "id": r[0],
            "content": r[1],
            "summary": r[2],
            "created_at": r[3]
        })

    return notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: int):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM notes WHERE id = %s RETURNING id;",
        (note_id,)
    )
    deleted = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if deleted:
        return {"message": "Note deleted"}
    else:
        return {"error": "Note not found"}
    
app.mount("/static", StaticFiles(directory="client"), name="static")

@app.put("/notes/{note_id}")
def update_note(note_id: int, note: NoteCreate):
    # regenerate summary
    summary = summarize_text(note.content)

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE notes SET content = %s, summary = %s WHERE id = %s RETURNING id;",
        (note.content, summary, note_id)
    )
    updated = cur.fetchone()

    conn.commit()
    cur.close()
    conn.close()

    if updated:
        return {
            "message": "Note updated",
            "id": note_id,
            "summary": summary
        }
    else:
        return {"error": "Note not found"}

@app.get("/app")
def serve_app():
    return FileResponse("client/index.html")