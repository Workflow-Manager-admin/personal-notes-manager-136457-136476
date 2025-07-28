"""Script for initial database setup for notes_backend."""
from app import app
from app.models import db

with app.app_context():
    db.create_all()
    print("Database tables created.")
