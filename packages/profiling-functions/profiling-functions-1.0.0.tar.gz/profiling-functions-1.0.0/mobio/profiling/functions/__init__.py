import os

import thriftpy
from thriftpy.rpc import make_client


def make_service(host, port):
    RESOURCE_OF_THRIFT, _ = os.path.split(os.path.abspath(__file__))
    thrift_path = RESOURCE_OF_THRIFT + "/client.thrift"
    profiling_client = thriftpy.load(thrift_path, module_name="p_thrift")

    global client
    client = make_client(profiling_client.ProfilingService, host, port)


def build_query(merchant_id, business_case_id, s_filter):
    if client:
        return client.build_query(merchant_id, business_case_id, s_filter)
    raise ModuleNotFoundError("No client here. Please run make_service first")
