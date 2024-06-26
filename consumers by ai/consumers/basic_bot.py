#https://pub.towardsai.net/real-time-sentiment-analysis-with-kafka-and-pyspark-145cd2338455
#https://community.aws/content/2iClhCY97xoQmZ0Uri8Sgd0bkC5/real-time-sentiment-analysis-with-kafka-and-sagemaker
from confluent_kafka import Producer, Consumer, KafkaError # to produce and consume data from Apache Kafka topics
import boto3 # to programmatically create, configure, and manage AWS resources
import json # to work with social media messages that are represented as JSON objects
import re # for helper functionality to clean HTML tags from social media messages

# Define a mapping dictionary to map model labels to negative/positive label
label_mapping = {'LABEL_0': 'negative', 'LABEL_1': 'positive'}
def read_config():
  # reads the client configuration from client.properties
  # and returns it as a key-value map
  config = {}
  with open("client.properties") as fh:
    for line in fh:
      line = line.strip()
      if len(line) != 0 and line[0] != "#":
        parameter, value = line.strip().split('=', 1)
        config[parameter] = value.strip()
  return config
 
def get_prediction(text):
    endpoint_name = 'jumpstart-dft-distilbert-tc-base-multilingual-cased'
    client = boto3.client('runtime.sagemaker')
    query_response = client.invoke_endpoint(EndpointName=endpoint_name, ContentType='application/x-text', Body=text, Accept='application/json;verbose')
    model_predictions = json.loads(query_response['Body'].read())
    probabilities, labels, predicted_label = model_predictions['probabilities'], model_predictions['labels'], model_predictions['predicted_label']
    # Map the predicted_label to your the label using the mapping dictionary
    predicted_label = label_mapping.get(predicted_label, predicted_label)
    return probabilities, labels, predicted_label

CLEANR = re.compile('<.*?>') 

def get_json_body(message):    
    decoded_message = message.value().decode('utf-8') # Decode from binary 
    json_message = json.loads(decoded_message)  # Parse JSON message
    return json_message

def get_clean_content(json_object):    
    content = json_object.get("content", "")  # Retrieve 'content' property    
    only_text = re.sub(CLEANR, '', content)
    return only_text

# Send a message to a Kafka topic
def send_message(message, topic_name, producer):
    producer.produce(topic_name, json.dumps(message).encode('utf-8'))
    producer.flush()
    
def send_enriched_data(message, probabilities, predicted_label, producer):
    message['probabilities'] = probabilities
    message['predition'] = predicted_label
    send_message(message, "apache_kafka_enriched_output_topic_name", producer)
    
def report_processing_error(message, error_code, error_message, producer):
    message['processing_error_code'] = error_code
    message['processing_error_message'] = error_message
    send_message(message, "apache_kafka_processing_errors_topic_name", producer)

def consume(topic, config):
    print("creating consumer")
    consumer = Consumer(config)
    print("subscribing to topic")
    consumer.subscribe(topic)
    print(f"Processing messages")
    while True:
        message = consumer.poll(1.0)  # Poll for messages, with a timeout of 1 second

        if message is None:
            continue

        if message.error():
            if message.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                print(f"Reached end of partition for topic {message.topic()} [{message.partition()}]")
            else:
                print(f"Error while consuming message: {message.error()}")
        else:
            # Process the message
            json_body = get_json_body(message)
            content_property = get_clean_content(json_body)
            if content_property == "":
                continue

            try:
                probabilities, labels, predicted_label = get_prediction(content_property)
                print(f"Inference:\n"
                    f"Input text: '{content_property}'\n"
                    f"Model prediction: {probabilities}\n"
                    f"Predicted label: {predicted_label}\n")

                send_enriched_data(json_body, probabilities, predicted_label, producer)
                

            except Exception as e:
                print(f"An error occurred: {e}")
                response = getattr(e, "response", {})
                error_code = response.get("Error", {}).get("Code", "Unknown")
                error_message = response.get("Error", {}).get("Message", "Unknown")
                report_processing_error(json_body, error_code, error_message, producer)
                

    # Close the consumer
    consumer.close()
def main():
  config = read_config()
  topic = "customer-chat"
  producer = Producer(config)
  consume(topic, config, producer)

main()