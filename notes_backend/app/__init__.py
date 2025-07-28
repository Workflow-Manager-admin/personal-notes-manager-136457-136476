from flask import Flask
from flask_cors import CORS
from .routes.health import blp
from flask_smorest import Api
from .models import db
from flask_jwt_extended import JWTManager
import os

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app, resources={r"/*": {"origins": "*"}})
app.config["API_TITLE"] = "My Flask API"
app.config["API_VERSION"] = "v1"
app.config["OPENAPI_VERSION"] = "3.0.3"
app.config['OPENAPI_URL_PREFIX'] = '/docs'
app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
# Database and JWT configuration
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("NOTES_DB_URI", "sqlite:///notes.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret-change-me")

# Initialize Flask extensions
db.init_app(app)
jwt = JWTManager(app)

api = Api(app)

# Register routes
api.register_blueprint(blp)

# Import and register user/note blueprints
from .routes.user import user_blp
from .routes.note import note_blp
api.register_blueprint(user_blp)
api.register_blueprint(note_blp)
