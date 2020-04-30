from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from azss.vars import context


def connect(connection_string=None):
    if connection_string is None:
        print("usage: connect connection_string")
    else:
        try:
            conn: BlobServiceClient = BlobServiceClient.from_connection_string(connection_string)
            containers = list(map(lambda x: x, conn.list_containers()))
            context.accounts[conn.account_name] = containers
            context.active_connections[conn.account_name] = conn
        except Exception as e:
            print(e)

