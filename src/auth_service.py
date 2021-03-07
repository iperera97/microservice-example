from concurrent import futures
from random import randrange

import grpc
from tinydb import TinyDB, Query

from generated import auth_pb2
from generated import auth_pb2_grpc


class AuthService(auth_pb2_grpc.AuthServiceServicer):

    db = TinyDB("db/auth.json")
    auth_table = db.table('users')

    def create_user(self, request, context):
        user_data = {
            "id": randrange(1, 1000),
            "email": request.email,
            "first_name": request.first_name,
            "last_name": request.last_name,
            "is_active": True
        }
        self.auth_table.insert(user_data)
        return auth_pb2.UserResponse(**user_data)

    def get_user(self, request, context):
        User = Query()
        user_query = self.auth_table.search(User.id == request.id)

        if len(user_query) == 0:
            context.abort(grpc.StatusCode.NOT_FOUND, "user not found")

        user_data = user_query[0]
        return auth_pb2.UserResponse(**user_data)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(
        AuthService(), server
    )
    server.add_insecure_port("[::]:5000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
