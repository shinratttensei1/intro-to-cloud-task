from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017"))
db = client["notesdb"]
notes = db["notes"]

HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>Cloud Notes</title>
    <style>
        body { font-family: sans-serif; max-width: 500px; margin: 50px auto; background: #f4f4f4; }
        .container { background: white; padding: 20px; border-radius: 8px; shadow: 0 2px 5px rgba(0,0,0,0.1); }
        input { width: 70%; padding: 10px; }
        button { padding: 10px; cursor: pointer; background: #007bff; color: white; border: none; }
        ul { list-style: none; padding: 0; }
        li { background: #eee; margin: 5px 0; padding: 10px; display: flex; justify-content: space-between; }
    </style>
</head>
<body>
    <div class="container">
        <h2>My Cloud Notes</h2>
        <input type="text" id="noteInput" placeholder="Write a note...">
        <button onclick="addNote()">Add</button>
        <ul id="noteList"></ul>
    </div>

    <script>
        async function loadNotes() {
            const res = await fetch('/notes');
            const data = await res.json();
            const list = document.getElementById('noteList');
            list.innerHTML = data.map(n => `<li>${n.text} <button onclick="deleteNote('${n._id}')">x</button></li>`).join('');
        }
        async function addNote() {
            const text = document.getElementById('noteInput').value;
            await fetch('/notes', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });
            document.getElementById('noteInput').value = '';
            loadNotes();
        }
        async function deleteNote(id) {
            await fetch(`/notes/${id}`, { method: 'DELETE' });
            loadNotes();
        }
        loadNotes();
    </script>
</body>
</html>
"""


def serialize(note):
    note["_id"] = str(note["_id"])
    return note


@app.route("/notes", methods=["GET"])
def get_notes():
    return jsonify([serialize(n) for n in notes.find()])


@app.route("/notes", methods=["POST"])
def create_note():
    data = request.get_json()
    if not data or not data.get("text"):
        return jsonify({"error": "text is required"}), 400
    result = notes.insert_one({"text": data["text"]})
    note = notes.find_one({"_id": result.inserted_id})
    return jsonify(serialize(note)), 201


@app.route("/notes/<note_id>", methods=["DELETE"])
def delete_note(note_id):
    result = notes.delete_one({"_id": ObjectId(note_id)})
    if result.deleted_count == 0:
        return jsonify({"error": "not found"}), 404
    return jsonify({"deleted": note_id})


@app.route("/")
def index():
    return render_template_string(HTML_UI)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
