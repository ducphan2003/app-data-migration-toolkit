from marshmallow import Schema, fields, validate

class MigrateQuizSchema(Schema):
    quiz_id = fields.String(required=True, validate=validate.Length(min=1))

class MigrationStatusSchema(Schema):
    process_id = fields.String(required=True)
    status = fields.String(required=True, validate=validate.OneOf(['pending', 'processing', 'completed', 'failed']))
    progress = fields.Float(required=True)
    message = fields.String(allow_none=True)
    result = fields.Dict(allow_none=True) 