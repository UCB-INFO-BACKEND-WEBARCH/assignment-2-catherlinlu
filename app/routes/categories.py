from flask import Blueprint, request, jsonify
from app import db
from app.models import Category, Tasks
from app.schemas import CategorySchema


categories = Blueprint('categories', __name__)
category_schema = CategorySchema()

@categories.route('/categories', methods=['GET'])
#returns all categories, w count of tasks in each
def get_all_categories():
    all_cats = Category.query.all()
    all = []
    for c in all_cats: 
        all.append({
            "id": c.id,
            "name": c.name, 
            "color": c.color, 
            "task_count": len(c.tasks)})
    return jsonify({"categories": all}), 200

@categories.route('/categories/:id', methods=['GET'])
def get_category(id): 
    category = Category.get_or_404(id)
    if not category: 
        return jsonify({"error": "404 Not Found"}), 404
    #tasks is just a pointer/related in categories, need to display what we want 
    cat_tasks = []
    for t in category.tasks:
        cat_tasks.append(
            {"id": t.id, 
             "title": t.title, 
             "completed": t.completed
            }
        )
    return jsonify(
        {"id": category.id, 
         "name": category.name,
         "color": category.color,
         "tasks": cat_tasks}), 200

@categories.route('/categories', methods=['POST'])
def create_category(): 
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({"error": "Name is required"}), 400
    errors = category_schema.validate(data)
    if errors:
        return jsonify({"errors": errors}), 400
    #check if name alr exists
    exists = Category.query.filter_by(name=data['name']).first()
    if exists: 
        return jsonify({"errors":{"name":["Category with this name already exists."]}}), 400
    category = Category(
        name = data['name'],
        color = data['color']
    )
    db.session.add(category)
    db.session.commit()
    return jsonify({ "name": category.name, "color": category.name})

@categories.route('/categories/:id', methods=['DELETE'])
def delete_category(id):
    category = Category.get_or_404(id)
    if not category: 
        return jsonify({"error": "Category not found"}), 404
    if len(category.tasks) > 0:
        return jsonify({"error": "Cannot delete category with existing tasks. Move or delete tasks first."}), 400
    db.session.delete(category)
    db.session.commit
    return jsonify({"message": "Category deleted"}), 200

