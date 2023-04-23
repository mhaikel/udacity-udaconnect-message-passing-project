import grpc

import location_event_pb2
import location_event_pb2_grpc

print("Sending Location Event ...")

channel = grpc.insecure_channel("127.0.0.1:30003")
stub = location_event_pb2_grpc.LocationEventServiceStub(channel)

# Add fake location data
user_coordinates = location_event_pb2.LocationEventMessage(
    userId=300,
    latitude=-100,
    longitude=30
)

user_coordinates_2 = location_event_pb2.LocationEventMessage(
    userId=400,
    latitude=-100,
    longitude=30
)

response_1 = stub.Create(user_coordinates)
response_2 = stub.Create(user_coordinates_2)


print("Coordinates sent...")
print(user_coordinates, user_coordinates_2)