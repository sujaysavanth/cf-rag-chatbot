from urllib.parse import urlparse
from workers import Response, WorkerEntrypoint
from submodule import get_hello_message

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)
        method = request.method

        if url.path == "/hello" and method == "GET":
            return Response(get_hello_message())
        if url.path == "/ingest" and method =="POST":
            return Response("Data ingested successfully", status=200)
        
        if url.path == "/query" and method == "GET":
            return Response("Query executed successfully",status = 200)

        return Response("Not found", status=404)