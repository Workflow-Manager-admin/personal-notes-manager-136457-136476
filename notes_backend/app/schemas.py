from marshmallow import Schema, fields, validate

# PUBLIC_INTERFACE
class UserRegisterSchema(Schema):
    """Schema for user registration."""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=64), description="Username")
    password = fields.Str(required=True, load_only=True, description="Password")

# PUBLIC_INTERFACE
class UserLoginSchema(Schema):
    """Schema for user login."""
    username = fields.Str(required=True, description="Username")
    password = fields.Str(required=True, load_only=True, description="Password")

# PUBLIC_INTERFACE
class UserResponseSchema(Schema):
    """Schema for responding with user information."""
    id = fields.Int()
    username = fields.Str()
    created_at = fields.DateTime()

# PUBLIC_INTERFACE
class NoteCreateSchema(Schema):
    """Schema for note creation."""
    title = fields.Str(required=True, validate=validate.Length(min=1, max=120))
    content = fields.Str(required=True)

# PUBLIC_INTERFACE
class NoteUpdateSchema(Schema):
    """Schema for updating a note."""
    title = fields.Str(validate=validate.Length(min=1, max=120))
    content = fields.Str()

# PUBLIC_INTERFACE
class NoteResponseSchema(Schema):
    """Schema for responding with note information."""
    id = fields.Int()
    title = fields.Str()
    content = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    user_id = fields.Int()

# PUBLIC_INTERFACE
class NoteQuerySchema(Schema):
    """Schema for note search/filter parameters."""
    title = fields.Str(description="Search notes by title (case-insensitive substring match)", required=False)
    content = fields.Str(description="Search notes by content (case-insensitive substring match)", required=False)
    page = fields.Int(missing=1)
    per_page = fields.Int(missing=10)
