from flask import Blueprint, request, jsonify
from app.services.migrate import MigrateService
from app.schemas.migrate_schema import MigrateQuizSchema
from app.repositories.migrate import MigrateRepository

def create_migrate_controllers(migrate_repo: MigrateRepository) -> Blueprint:
  migrate_controller = Blueprint('migrate', __name__)
  migrate_service = MigrateService(
    migrate_repo=migrate_repo
  )

  @migrate_controller.route('/migrate', methods=['GET'])
  def migrate():
    return jsonify({'message': 'Migration started successfully'}), 200

  return migrate_controller
