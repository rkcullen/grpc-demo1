from concurrent import futures
import logging

from tad import anomaly_detect_ts
import grpc

import json
import pandas as pd
from io import StringIO

import detection_types_pb2 as anomalies_types 
import anomaly_detection_pb2_grpc as anomalies_service

class AnomalyDetectionService(anomalies_service.AnomalyDetectionServicer):

    def dparserfunc(self, date):
        return pd.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')

    def TwitterAnomalies(self, request_iterator, context):
        for msq in request_iterator:
            raw_csv = StringIO(msq.raw_json)
            only_last = msq.only_last
            data1 = pd.read_csv(raw_csv, index_col='timestamp', parse_dates=True, squeeze=True, date_parser=self.dparserfunc) 
            result = anomaly_detect_ts(data1, alpha=0.05, direction="both", only_last=only_last, plot=False, longterm=True)

            for key in result["anoms"].to_dict():
                keypair = anomalies_types.KeyValuePair(
                    timestamp=key.strftime('%Y-%m-%d %H:%M:%S'), value=result['anoms'][key]
                )   
                yield anomalies_types.Response(keypair=keypair)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    anomalies_service.add_AnomalyDetectionServicer_to_server(AnomalyDetectionService(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
