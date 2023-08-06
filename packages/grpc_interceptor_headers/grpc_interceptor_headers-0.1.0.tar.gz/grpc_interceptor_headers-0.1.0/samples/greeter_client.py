# Copyright 2017 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""The Python implementation of the GRPC helloworld.Greeter client."""

import grpc
from . import helloworld_pb2
from . import helloworld_pb2_grpc

from grpc_interceptor_headers.header_manipulator_client_interceptor import header_adder_interceptor


def do_call(bind="0.0.0.0:50051",
            header_name="abc",
            header_content="def",
            name="you"):
    header_interceptor = header_adder_interceptor(header_name, header_content)

    with grpc.insecure_channel(bind) as channel:
        intercept_channel = grpc.intercept_channel(channel, header_interceptor)
        stub = helloworld_pb2_grpc.GreeterStub(intercept_channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name=name))
    return response.message
