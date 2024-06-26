from confluent_kafka import Consumer, KafkaError
import socket
import requests

# Kafka consumer configuration
conf = {
    'bootstrap.servers': 'your_kafka_broker:9092',  # Replace with actual broker address
    'group.id': 'my-consumer-group',
    'auto.offset.reset': 'earliest',
    'client.id': socket.gethostname(),
}

# Create a Kafka consumer
consumer = Consumer(conf)
consumer.subscribe(['customer-chat'])  # Subscribe to the customer-chat topic

# Anthropic API endpoint
ANTHROPIC_API_URL = 'https://api.anthropic.com/messages'

def analyze_sentiment(message_content):
    # Send message content to Anthropic API for sentiment analysis
    response = requests.post(ANTHROPIC_API_URL, json={'messages': [{'role': 'user', 'content': message_content}]})
    sentiment_score = response.json().get('messages')[0].get('sentiment')
    return sentiment_score

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

        # Decide whether to notify humans based on sentiment (you can customize this logic)
        if sentiment_score == 'negative':
            # Produce a notification to the notify-human topic
            # Implement your Kafka producer logic here
            print(f"Negative sentiment detected: {message_content}")

if __name__ == '__main__':
    main()
