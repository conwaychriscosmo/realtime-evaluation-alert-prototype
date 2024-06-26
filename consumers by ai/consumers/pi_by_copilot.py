from confluent_kafka import Consumer, KafkaError, Producer
import requests
import json

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'your_kafka_broker:9092',  # Replace with actual broker address
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'client.id': 'kafka-consumer',
}

# Create a Kafka consumer
consumer = Consumer(conf)
consumer.subscribe(['customer-chat'])  # Subscribe to the customer-chat topic

# Inflection Pi API endpoint
INFLECTION_API_URL = 'https://api.inflection.ai/messages'

# Kafka producer configuration
producer_conf = {
    'bootstrap.servers': 'your_kafka_broker:9092',  # Replace with actual broker address
    'client.id': 'kafka-producer',
}

# Create a Kafka producer
producer = Producer(producer_conf)
notify_topic = 'notify-human'  # Replace with your desired topic name

def analyze_sentiment(message_content):
    try:
        response = requests.post(INFLECTION_API_URL, json={'messages': [{'role': 'user', 'content': message_content}]})
        response_data = response.json()
        sentiment_score = response_data['messages'][0]['sentiment']
        return sentiment_score
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None

def main():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Extract message content
        message_content = msg.value().decode('utf-8')

        # Analyze sentiment
        sentiment_score = analyze_sentiment(message_content)

        if sentiment_score:
            # Produce a notification if sentiment indicates a problem
            if 'negative' in sentiment_score.lower():
                try:
                    producer.produce(notify_topic, key=None, value=message_content)
                    producer.flush()
                    print(f"Negative sentiment detected: {message_content}")
                except Exception as e:
                    print(f"Error producing notification: {e}")

if __name__ == '__main__':
    main()
