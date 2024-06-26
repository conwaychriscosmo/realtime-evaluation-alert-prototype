from confluent_kafka import Consumer, KafkaError
import requests

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

# OpenAI API endpoint
OPENAI_API_URL = 'https://api.openai.com/v1/engines/davinci/completions'

def analyze_sentiment(message_content):
    # Send message content to OpenAI API for sentiment analysis
    response = requests.post(OPENAI_API_URL, json={
        'prompt': message_content,
        'max_tokens': 50,  # Adjust as needed
    }, headers={'Authorization': 'Bearer YOUR_OPENAI_API_KEY'})
    sentiment_score = response.json().get('choices')[0].get('text')
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

        # Decide whether to notify humans based on sentiment (customize this logic)
        if 'negative' in sentiment_score.lower():
            # Produce a notification to the notify-human topic
            # Implement your Kafka producer logic here
            print(f"Negative sentiment detected: {message_content}")

if __name__ == '__main__':
    main()
