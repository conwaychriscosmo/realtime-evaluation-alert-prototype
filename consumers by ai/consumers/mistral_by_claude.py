import json
from kafka import KafkaConsumer
import requests
import os

# Kafka configuration
KAFKA_TOPIC = 'customer_service_messages'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']  # Adjust as needed

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
MISTRAL_API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def analyze_sentiment_mistral(text):
    try:
        prompt = f"Analyze the sentiment of the following text and respond with only one word: 'positive', 'negative', or 'neutral'. Text: '{text}'"
        response = requests.post(MISTRAL_API_URL, headers=headers, json={"inputs": prompt})
        result = response.json()
        # Extract the sentiment from the response
        sentiment = result[0]['generated_text'].strip().lower()
        return sentiment if sentiment in ['positive', 'negative', 'neutral'] else 'unknown'
    except Exception as e:
        print(f"Error in Mistral sentiment analysis: {e}")
        return "unknown"

def process_message(msg):
    try:
        data = json.loads(msg.value.decode('utf-8'))
        text = data.get('message', '')
        
        sentiment = analyze_sentiment_mistral(text)
        
        print(f"Message: {text}")
        print(f"Mistral Sentiment: {sentiment}")
        print("---")
        
    except json.JSONDecodeError:
        print(f"Error decoding message: {msg.value}")
    except Exception as e:
        print(f"Error processing message: {e}")

def main():
    consumer = KafkaConsumer(
        KAFKA_TOPIC,
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        auto_offset_reset='latest',
        enable_auto_commit=True,
        group_id='mistral_sentiment_analysis_group'
    )

    print("Mistral Sentiment analysis consumer started. Waiting for messages...")

    for message in consumer:
        process_message(message)

if __name__ == "__main__":
    main()