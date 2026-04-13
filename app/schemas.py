from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models import Category
#provide validation rules -> marshmallow checks for validation & generates error message
class CategorySchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=50))
    color = fields.Str(validate=validate.Regexp(r'^#[0-9A-Fa-f]{6}$'))

class TaskSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    description = fields.Str(validate=validate.Length(max=500))
    completed = fields.Bool()
    due_date = fields.DateTime(format='iso')
    category_id = fields.Int()
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)