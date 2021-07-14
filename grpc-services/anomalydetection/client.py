import anomaly_detection_pb2_grpc as anomalies_service
import detection_types_pb2 as anomalies_types
from client_wrapper import ServiceClient
from os import walk

def make_request():
    filenames = next(walk("files"), (None, None, []))[2]
    for fn in filenames:
        with open('files/' + fn, "r") as f:
            data1 = f.read() + "\n"
            request = anomalies_types.Request(
                raw_json=data1, only_last='day'
            )
        return request

def generate_requests():
    requests = [
        make_request()
    ]

    for req in requests:
        yield req

def run():
    anomalies = ServiceClient(anomalies_service, 'AnomalyDetectionStub', 'localhost', 50051)
    # Insert example metadata
    metadata = [('ip', '127.0.0.1')]
    response = anomalies.TwitterAnomalies(generate_requests())
    for resp in response:
        print(resp)


if __name__ == '__main__':
    run()
