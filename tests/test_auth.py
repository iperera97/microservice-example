import pytest
import grpc

from generated.auth_pb2 import CreateUserRequest, GetUserRequest
from generated.auth_pb2_grpc import AuthServiceStub

@pytest.fixture(scope="module")
def connection():
    channel = grpc.insecure_channel("localhost:5000")
    client = AuthServiceStub(channel)
    yield client

def test_create_user(connection):
    request = CreateUserRequest(
        email="kasun@gmail.com",
        first_name="kasun",
        last_name="perera",
        password="kasun@123",
    )
    response = connection.create_user(request)
    print("response", response)


def test_get_user(connection):
    request = GetUserRequest(id=158)
    response = connection.get_user(request)
    print("get user", response)
