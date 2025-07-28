from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

from ..models import db, User
from ..schemas import (
    UserRegisterSchema,
    UserLoginSchema,
    UserResponseSchema
)

user_blp = Blueprint(
    "User",
    "user",
    url_prefix="/api/user",
    description="Endpoints for user registration, login, and account info."
)


@user_blp.route("/register")
class Register(MethodView):
    """Endpoint to register a new user."""
    @user_blp.arguments(UserRegisterSchema)
    @user_blp.response(201, UserResponseSchema)
    def post(self, user_data):
        if User.query.filter_by(username=user_data["username"]).first():
            abort(409, message="Username already taken.")
        user = User(username=user_data["username"])
        user.set_password(user_data["password"])
        db.session.add(user)
        db.session.commit()
        return user


@user_blp.route("/login")
class Login(MethodView):
    """Endpoint to authenticate and login a user."""
    @user_blp.arguments(UserLoginSchema)
    def post(self, login_data):
        user = User.query.filter_by(username=login_data["username"]).first()
        if user and user.check_password(login_data["password"]):
            access_token = create_access_token(identity=user.id)
            return {"access_token": access_token, "user": UserResponseSchema().dump(user)}
        abort(401, message="Invalid username or password.")


@user_blp.route("/me")
class UserProfile(MethodView):
    """Get details for the authenticated user."""
    @jwt_required()
    @user_blp.response(200, UserResponseSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user:
            abort(404, message="User not found.")
        return user
