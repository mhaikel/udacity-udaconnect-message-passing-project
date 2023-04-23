import json
import os
import logging

from concurrent import futures
from kafka import KafkaProducer

import grpc

import location_event_pb2
import location_event_pb2_grpc

kafka_url = os.environ["KAFKA_SERVER"]
kafka_topic = os.environ["TOPIC_NAME"]

logging.info('initiating connection to kafka ', kafka_url)
print('p_connecting to kafka ', kafka_url)
logging.info('initiating connection to kafka topic ', kafka_topic)
print('p_connecting to kafka topic ', kafka_topic)

producer = KafkaProducer(bootstrap_servers=kafka_url)


class LocationEventServicer(location_event_pb2_grpc.LocationEventServiceServicer):

    def Create(self, request, context):
        request_value = {
            'userId': int(request.userId),
            'latitude': int(request.latitude),
            'longitude': int(request.longitude)
        }

        logging.info('processing entity ', request_value)

        user_encode_data = json.dumps(request_value, indent=2).encode('utf-8')
        producer.send(kafka_topic, user_encode_data)
        return location_event_pb2.LocationEventMessage(**request_value)


server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
location_event_pb2_grpc.add_LocationEventServiceServicer_to_server(LocationEventServicer(), server)

logging.info('starting on port 5005')
server.add_insecure_port('[::]:5005')
server.start()
server.wait_for_termination()