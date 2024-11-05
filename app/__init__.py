from flask import Flask

from app.db.base import create_db
from app.routes.room import room_blueprint


app = Flask(__name__)
app.register_blueprint(room_blueprint)


def main():
    create_db()
    app.run(debug=True, port=80)
