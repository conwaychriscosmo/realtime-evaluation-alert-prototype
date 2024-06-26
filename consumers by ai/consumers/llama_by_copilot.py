from confluent_kafka import Consumer, KafkaError
import requests

# Kafka consumer configuration (replace with actual details)
conf = {
    'bootstrap.servers': 'your_kafka_broker:9092',
    'group.id': 'llama-consumer-group',
    'auto.offset.reset': 'earliest',
    'client.id': 'llama-consumer',
}

# Create a Kafka consumer
consumer = Consumer(conf)
consumer.subscribe(['customer-chat'])

# LLAMA API endpoint (replace with actual endpoint)
LLAMA_API_URL = 'https://api.llama.ai/sentiment'

def analyze_sentiment(message_content):
    try:
        response = requests.post(LLAMA_API_URL, json={'text': message_content})
        sentiment_score = response.json().get('sentiment')
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

        if sentiment_score and 'negative' in sentiment_score.lower():
            # Produce a notification to the notify-human topic
            # Implement your Kafka producer logic here
            print(f"Negative sentiment detected: {message_content}")

if __name__ == '__main__':
    main()
