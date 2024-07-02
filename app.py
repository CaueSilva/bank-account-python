from flask import Flask
from controller import api
from config.db_config import db, url_db

app = Flask(__name__)
api.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = url_db
db.init_app(app)

if __name__ == "__main__":
    app.run(debug=True)
