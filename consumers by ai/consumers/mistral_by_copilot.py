# Similar setup as before (replace with actual details)
# ...

# Mistral API endpoint (replace with actual endpoint)
MISTRAL_API_URL = 'https://api.mistral.ai/sentiment'

def analyze_sentiment_mistral(message_content):
    try:
        response = requests.post(MISTRAL_API_URL, json={'text': message_content})
        sentiment_score = response.json().get('sentiment')
        return sentiment_score
    except Exception as e:
        print(f"Error analyzing sentiment with Mistral: {e}")
        return None

def main_mistral():
    while True:
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue

        # Extract message content
        message_content = msg.value().decode('utf-8')

        # Analyze sentiment with Mistral
        sentiment_score = analyze_sentiment_mistral(message_content)

        if sentiment_score and 'negative' in sentiment_score.lower():
            # Produce a notification to the notify-human topic
            # Implement your Kafka producer logic here
            print(f"Negative sentiment detected (Mistral): {message_content}")

if __name__ == '__main__':
    main_mistral()
