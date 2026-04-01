from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import os

app = Flask(__name__)

client = MongoClient(os.environ.get("MONGO_URI", "mongodb://localhost:27017"))
db = client["notesdb"]
notes = db["notes"]


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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)
