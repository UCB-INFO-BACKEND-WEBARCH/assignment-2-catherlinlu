from flask import Blueprint, request, jsonify
from app import db
from app.models import Category, Tasks
from datetime import datetime, timezone
from app.schemas import TaskSchema
from app import task_queue  #import queue
from app.jobs import send_due_date_notification
from datetime import datetime, timezone, timedelta
task_schema = TaskSchema()

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks', methods=['GET'])
def get_all_tasks():
    completed_filter = request.args.get('completed')
    if completed_filter is not None: 
        complete = completed_filter.lower() == 'true'
        all_tasks = Tasks.query.filter(completed = complete).all()
    else: 
        all_tasks = Tasks.query.all()
    result = []
    for t in all_tasks:
        result.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "due_date": t.due_date.isoformat() if t.due_date else None,
            "category_id": t.category_id,
            "category": {
                "id": t.category.id,
                "name": t.category.name,
                "color": t.category.color
            } if t.category else None,
            "created_at": t.created_at.isoformat(),
            "updated_at": t.updated_at.isoformat()
            })
    return jsonify ({"tasks": result}), 200

@tasks_bp.route('/tasks/:id', methods=['GET'])
def get_task(id):
    task = Tasks.get_or_404(id)
    if not task: 
        return jsonify({"error": "Task not found"}), 404
    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "category_id": task.category_id,
        "category": {
            "id": task.category.id,
            "name": task.category.name,
            "color": task.category.color
        } if task.category else None,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }), 200

@tasks_bp.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    errors = task_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400 #marshmallow generates messages based on requirements
    #category must reference existing 
    if data.get('category_id'): 
        if not Category.query.get(data['category_id']):
            return jsonify({"error: Must reference an existing category"}), 400
    due_date = None
    if data.get("due_date"):
        due_date = datetime.fromisoformat(data["due_date"].replace('Z', '+00:00'))

    task = Tasks(
        title= data.get("title"),
        description= data.get("description"), 
        due_date= due_date,
        category_id= data.get("category_id"))
    
    db.session.add(task)
    db.session.commit() #add and commit to database
    
    #notifications
    notification_queued = False
    if task.due_date:  #check if due date exists
        now = datetime.utcnow()
        time_until_due = task.due_date - now
        
        #only queue if due in the future AND in less than 24 hrs
        if timedelta(0) < time_until_due <= timedelta(hours=24):
            task_queue.enqueue(send_due_date_notification, task.title)
            notification_queued = True

    return jsonify({"task" : {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "due_date": task.due_date,
        "category_id": task.category_id,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
        },
        "notification_queued": notification_queued  #placeholder
        }), 201

@tasks_bp.route('/tasks/:id', methods=['PUT'])
def update_task(id):
    task = Tasks.get_or_404(id)
    if not task: 
        return jsonify({"error":"Task Not Found"}), 404
    data = request.get_json()
    
    #validation:
    errors = task_schema.validate(data, partial=True) #not everything is required
    if errors:
        return jsonify({"errors": errors}), 400
    #checking to see what data needs me to change
    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'completed' in data:
        task.completed = data['completed']
    if 'due_date' in data:
        task.due_date = data['due_date']
    if 'category_id' in data:
        # check if category exists
        if not Category.query.get(data['category_id']):
            return jsonify({"errors": {"category_id": ["Category not found."]}}), 400
        task.category_id = data['category_id']
    
    db.session.commit()

    return jsonify({
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "completed": task.completed,
        "due_date": task.due_date,
        "category_id": task.category_id,
        "created_at": task.created_at.isoformat(),
        "updated_at": task.updated_at.isoformat()
    }), 200

@tasks_bp.route('/tasks/:id', methods=['DELETE'])
def delete_task(id):
    task = Tasks.query.get_or_404(id)
    if not task:
        return jsonify({"error": "Task not found"}), 404    
    db.session.delete(task)
    db.session.commit()
    return jsonify({"message": "Task deleted"}), 200




