from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from redis import Redis
from rq import Queue

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db' #connecting the database to our tasks db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app) #set up database

migrate = Migrate(app, db)
app.config['REDIS_URL'] = 'redis://localhost:6379'
redis_conn = Redis.from_url(app.config['REDIS_URL'])
task_queue = Queue(connection=redis_conn)

from app.routes.tasks import tasks_bp
from app.routes.categories import categories
app.register_blueprint(tasks_bp)
app.register_blueprint(categories)
