import anomaly_detection_pb2_grpc as anomalies_service
import detection_types_pb2 as anomalies_types
from client_wrapper import ServiceClient
from os import walk

def read_files():
    file_list = []
    filenames = next(walk("files"), (None, None, []))[2]
    for fn in filenames:
        with open('files/' + fn, "r") as f:
            data1 = f.read() + "\n"
            request = anomalies_types.Request(
                raw_json=data1, only_last='day'
            )
        file_list.append(request)

    return file_list

def generate_requests():

    for req in read_files():
        yield req

def run():
    anomalies = ServiceClient(anomalies_service, 'AnomalyDetectionStub', 'localhost', 50051)
    # Insert example metadata
    metadata = [('ip', '127.0.0.1')]
    responses = anomalies.TwitterAnomalies(generate_requests())
    for resp in responses:
        print(resp)


if __name__ == '__main__':
    run()
