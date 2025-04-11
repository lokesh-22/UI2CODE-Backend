from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config import Config
from models import db
from routes import register_routes
from routes.car_review_routes import car_routes



load_dotenv()

app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)

@app.before_request
def create_tables_once():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True

register_routes(app)

app.register_blueprint(car_routes)

if __name__ == '__main__':
    app.run(debug=True)
