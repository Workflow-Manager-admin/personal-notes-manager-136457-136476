from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


# PUBLIC_INTERFACE
class User(db.Model):
    """User model for authentication and ownership of notes."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    notes = db.relationship('Note', backref='user', lazy='dynamic', cascade="all, delete-orphan")

    # PUBLIC_INTERFACE
    def set_password(self, password):
        """Hashes and sets user's password."""
        self.password_hash = generate_password_hash(password)

    # PUBLIC_INTERFACE
    def check_password(self, password):
        """Verifies provided password against stored hash."""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


# PUBLIC_INTERFACE
class Note(db.Model):
    """Model for storing user's notes."""
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"<Note {self.title} by user {self.user_id}>"
