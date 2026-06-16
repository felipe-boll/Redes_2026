import os
from datetime import datetime, timezone

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
db = SQLAlchemy(app)


class Message(db.Model):
    __tablename__ = "messages"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    ip_client = db.Column(db.String(45), nullable=True)  # IP informado no payload
    ip_origin = db.Column(db.String(45), nullable=True)  # IP real da conexão TCP com o backend
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


with app.app_context():
    db.create_all()


@app.get("/healthcheck")
def healthcheck():
    return jsonify({"status": "ok"})


@app.get("/messages")
def list_messages():
    messages = Message.query.order_by(Message.created_at.desc()).all()
    return jsonify([
        {
            "id": m.id,
            "name": m.name,
            "text": m.text,
            "ip_client": m.ip_client,
            "ip_origin": m.ip_origin,
            "created_at": m.created_at.isoformat(),
        }
        for m in messages
    ])


@app.post("/messages")
def create_message():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("text"):
        return jsonify({"error": "campos 'name' e 'text' são obrigatórios"}), 400
    msg = Message(
        name=data["name"],
        text=data["text"],
        ip_client=data.get("ip_client"),
        ip_origin=request.remote_addr,
    )
    db.session.add(msg)
    db.session.commit()
    return jsonify({"id": msg.id}), 201


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
