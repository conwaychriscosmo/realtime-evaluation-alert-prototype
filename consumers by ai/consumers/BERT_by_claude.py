import json
from kafka import KafkaConsumer
import requests
import os

# Kafka configuration
KAFKA_TOPIC = 'customer_service_messages'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']  # Adjust as needed

# Hugging Face API configuration
HUGGINGFACE_API_KEY = os.environ.get('HUGGINGFACE_API_KEY')
BERT_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"

headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}

def analyze_sentiment_bert(text):
    try:
        response = requests.post(BERT_API_URL, headers=headers, json={"inputs": text})
        result = response.json()
        # The API returns a list of dictionaries, we take the first one
        sentiment = max(result[0], key=lambda x: x['score'])['label']
        return 'positive' if sentiment == 'LABEL_1' else 'negative'
    except Exception as e:
        print(f"Error in BERT sentiment analysis: {e}")
        return "unknown"

def process_message(msg):
    try:
        data = json.loads(msg.value.decode('utf-8'))
        text = data.get('message', '')
        
        sentiment = analyze_sentiment_bert(text)
        
        print(f"Message: {text}")
        print(f"BERT Sentiment: {sentiment}")
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
        group_id='bert_sentiment_analysis_group'
    )

    print("BERT Sentiment analysis consumer started. Waiting for messages...")

    for message in consumer:
        process_message(message)

if __name__ == "__main__":
    main()