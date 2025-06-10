import pika
from app.utils.const import *
from app.repositories.rabbitmq import RabbitmqRepository


class MessageService:
    def __init__(
        self, 
        rabbitmq_repo: RabbitmqRepository
    ):
        # Initialize services
        self.rabbitmq_repo = rabbitmq_repo

    def send_message(
        self, 
        exchange: str, 
        queue: str, 
        message: any, 
        headers: dict = None
    ):
        self.rabbitmq_repo.send_message(
            exchange, 
            queue, 
            message, 
            headers
        )

    def receive_messages(
        self, 
        queue: str, 
        callback: any
    ):
        self.rabbitmq_repo.receive_messages(
            queue, 
            callback
        )

    def start_consuming(self):
        self.rabbitmq_repo.start_consuming()