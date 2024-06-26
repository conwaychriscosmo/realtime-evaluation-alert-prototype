import json
from kafka import KafkaConsumer
import anthropic  # You'll need to install this library
import os

# Kafka configuration
KAFKA_TOPIC = 'customer_service_messages'
KAFKA_BOOTSTRAP_SERVERS = ['localhost:9092']  # Adjust as needed

# Anthropic API configuration
ANTHROPIC_API_KEY = os.environ.get('ANTHROPIC_API_KEY')
client = anthropic.Client(api_key=ANTHROPIC_API_KEY)

def analyze_sentiment(text):
    try:
        # This is a hypothetical API call. You'll need to adjust based on actual Anthropic API
        response = client.completions.create(
            model="claude-2",  # or whatever the current model is
            prompt=f"Analyze the sentiment of the following text: '{text}'. Respond with only one word: 'positive', 'negative', or 'neutral'.",
            max_tokens_to_sample=1,
            temperature=0
        )
        return response.completion.strip()
    except Exception as e:
        print(f"Error in sentiment analysis: {e}")
        return "unknown"

def process_message(msg):
    try:
        # Assuming the message is in JSON format
        data = json.loads(msg.value.decode('utf-8'))
        text = data.get('message', '')
        
        sentiment = analyze_sentiment(text)
        
        # Here you would typically store or forward the results
        print(f"Message: {text}")
        print(f"Sentiment: {sentiment}")
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
        group_id='sentiment_analysis_group'
    )

    print("Sentiment analysis consumer started. Waiting for messages...")

    for message in consumer:
        process_message(message)

if __name__ == "__main__":
    main()