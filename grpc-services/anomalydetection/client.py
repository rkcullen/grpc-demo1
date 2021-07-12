import anomaly_detection_pb2_grpc as anomalies_service
import detection_types_pb2 as anomalies_types
from client_wrapper import ServiceClient


def run():
    anomalies = ServiceClient(anomalies_service, 'AnomaliesStub', 'localhost', 50051)
    # Insert example metadata
    metadata = [('ip', '127.0.0.1')]
    with open('test_data_1.csv', "r") as f:
        data1 = f.read() + "\n"
        request = anomalies_types.Request(
            raw_json=data1, only_last='day'
        )
    response = anomalies.TwitterAnomalies(request)
    for resp in response:
        print(resp)


if __name__ == '__main__':
    run()
