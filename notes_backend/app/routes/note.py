from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..models import db, Note
from ..schemas import (
    NoteCreateSchema,
    NoteUpdateSchema,
    NoteResponseSchema,
    NoteQuerySchema
)

note_blp = Blueprint(
    "Notes",
    "notes",
    url_prefix="/api/notes",
    description="Endpoints for creating, managing, and searching notes."
)

# PUBLIC_INTERFACE
@note_blp.route("/")
class NotesList(MethodView):
    """Create a new note or list/search notes for the user."""

    @jwt_required()
    @note_blp.arguments(NoteQuerySchema, location="query")
    @note_blp.response(200, NoteResponseSchema(many=True))
    def get(self, query_params):
        """
        List notes with optional search/filter for the authenticated user.
        ---
        Allows filtering by title/content, and supports pagination.
        """
        user_id = get_jwt_identity()
        query = Note.query.filter_by(user_id=user_id)
        # Filtering
        title = query_params.get("title")
        content = query_params.get("content")
        if title:
            query = query.filter(Note.title.ilike(f"%{title}%"))
        if content:
            query = query.filter(Note.content.ilike(f"%{content}%"))
        # Pagination
        page = query_params.get("page", 1)
        per_page = query_params.get("per_page", 10)
        notes_paged = query.order_by(Note.updated_at.desc()).paginate(page=page, per_page=per_page, error_out=False)
        return notes_paged.items

    @jwt_required()
    @note_blp.arguments(NoteCreateSchema)
    @note_blp.response(201, NoteResponseSchema)
    def post(self, note_data):
        """Create a note for authenticated user."""
        user_id = get_jwt_identity()
        note = Note(
            title=note_data["title"],
            content=note_data["content"],
            user_id=user_id
        )
        db.session.add(note)
        db.session.commit()
        return note

# PUBLIC_INTERFACE
@note_blp.route("/<int:note_id>")
class NotesDetail(MethodView):
    """CRUD operations on a single note."""

    @jwt_required()
    @note_blp.response(200, NoteResponseSchema)
    def get(self, note_id):
        """Get a single note by ID (only if owned by user)."""
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")
        return note

    @jwt_required()
    @note_blp.arguments(NoteUpdateSchema)
    @note_blp.response(200, NoteResponseSchema)
    def put(self, note_data, note_id):
        """Update an existing note (title/content; only if owned by user)."""
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")
        if "title" in note_data:
            note.title = note_data["title"]
        if "content" in note_data:
            note.content = note_data["content"]
        db.session.commit()
        return note

    @jwt_required()
    def delete(self, note_id):
        """Delete a note (only if owned by user)."""
        user_id = get_jwt_identity()
        note = Note.query.filter_by(id=note_id, user_id=user_id).first()
        if not note:
            abort(404, message="Note not found.")
        db.session.delete(note)
        db.session.commit()
        return {"message": "Note deleted."}
