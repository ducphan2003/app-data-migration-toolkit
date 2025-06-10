import pika
import json

# Thông tin kết nối RabbitMQ
RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_USER = 'guest'
RABBITMQ_PASS = 'guest'
RABBITMQ_EXCHANGE = 'prompting_exchange'
RABBITMQ_QUEUE_TASKS = 'prompting_tasks'

# Khởi tạo thông điệp
message = {
    "data": 
            {"input":"Overall, it is noticeable that the figure for 4 types of mobile packets  had a significant changes over the year , meanwhile we witnessed the most dramatic decrease in the second bracket.\nFirstly, the number of people using DOMO witnessed the slight increase from January to March about 18 euros , however it dropped 17 euros in the following year , and reach the peak at almost 20 euros in July.\n\nBetween July and September we witnessed the most substantial trend  of four different mobile , DOMO continuously decreased in 3 months in a row , at 20 euros in September , Meanwhile Lex was  remained stable in July to August and increase one last year to 18  euros.",
             "type":"LR_GR_TASK_1",
             "question":"During holidays or weekends, young people spend less time on outdoor activities in the natural environment, such as hiking and mountain climbing. Why? What can be done to encourage them to go out?",
             "answer_id":"123123"
    }
}

# Hàm gửi thông điệp đến RabbitMQ
def send_message():
    try:
        # Thiết lập thông tin xác thực
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASS)
        
        # Thiết lập kết nối
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=credentials
            )
        )
        channel = connection.channel()

        # Gửi thông điệp
        channel.basic_publish(
            exchange=RABBITMQ_EXCHANGE,
            routing_key=RABBITMQ_QUEUE_TASKS,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                headers=None,
                delivery_mode=2  # Lưu thông điệp bền vững (persistent)
            )
        )
        print(f" [x] Sent message with routing_key '{RABBITMQ_QUEUE_TASKS}' to exchange '{RABBITMQ_EXCHANGE}'")

    except pika.exceptions.AMQPConnectionError as error:
        print(f"Failed to connect to RabbitMQ: {error}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        # Đóng kết nối nếu đã được mở
        if 'connection' in locals() and connection.is_open:
            connection.close()
            print(" [x] Connection closed")

# Gọi hàm để gửi thông điệp
if __name__ == "__main__":
    send_message()