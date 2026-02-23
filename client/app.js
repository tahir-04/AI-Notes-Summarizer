const API_URL = "http://127.0.0.1:8000";
let allNotes = [];
// Load notes on page start
window.onload = loadNotes;

async function loadNotes() {
    const res = await fetch(`${API_URL}/notes`);
    const notes = await res.json();

    const list = document.getElementById("notesList");
    list.innerHTML = "";

    notes.forEach(n => {

        const div = document.createElement("div");
        div.className = "note";

        div.innerHTML = `
            <div class="note-content">
                <strong>Note:</strong><br>
                <span id="text-${n.id}">${n.content}</span>
            </div>

            <div class="note-summary">
                <strong>Summary:</strong><br>
                <span id="summary-${n.id}">${n.summary || "No summary"}</span>
            </div>

            <button onclick="editNote(${n.id})">Edit</button>
            <button class="delete-btn" onclick="deleteNote(${n.id})">Delete</button>
        `;

        list.appendChild(div);
    });

    allNotes = notes;
    renderNotes(notes);
}

function renderNotes(notes) {
    const list = document.getElementById("notesList");
    list.innerHTML = "";

    notes.forEach(n => {
        const div = document.createElement("div");
        div.className = "note";

        div.innerHTML = `
            <div class="note-content">
                <strong>Note:</strong><br>
                <span id="text-${n.id}">${n.content}</span>
            </div>

            <div class="note-summary">
                <strong>Summary:</strong><br>
                <span id="summary-${n.id}">${n.summary || "No summary"}</span>
            </div>

            <button onclick="editNote(${n.id})">Edit</button>
            <button class="delete-btn" onclick="deleteNote(${n.id})">Delete</button>
        `;

        list.appendChild(div);
    });
}

function filterNotes() {
    const query = document.getElementById("searchInput").value.toLowerCase();

    const filtered = allNotes.filter(n =>
        n.content.toLowerCase().includes(query) ||
        (n.summary && n.summary.toLowerCase().includes(query))
    );

    renderNotes(filtered);
}

async function addNote() {
    const text = document.getElementById("noteInput").value;
    if (!text) return;

    const res = await fetch(`${API_URL}/notes`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: text })
    });

    const data = await res.json();

    document.getElementById("noteInput").value = "";
    loadNotes();
}

async function deleteNote(id) {
    await fetch(`${API_URL}/notes/${id}`, {
        method: "DELETE"
    });

    loadNotes();
}

async function editNote(id) {
    const currentText = document.getElementById(`text-${id}`).innerText;

    const newText = prompt("Edit your note:", currentText);
    if (!newText) return;

    const res = await fetch(`${API_URL}/notes/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ content: newText })
    });

    const data = await res.json();

    loadNotes();
}