import json
from urllib.parse import urlparse
from workers import Response, WorkerEntrypoint
from ingest import handle_ingest
from query import handle_query

class Default(WorkerEntrypoint):
    async def fetch(self, request):
        url = urlparse(request.url)
        method = request.method

        if url.path == "/hello" and method == "GET":
            return Response("Hello World!")

        if url.path == "/ingest" and method == "POST":
            ingest_data = await request.json()
            response = await handle_ingest(ingest_data, self.env)
            return Response(f"Data ingested successfully: {response}", status=200)

        if url.path == "/query" and method == "GET":
            query = url.query
            response = await handle_query(query, self.env)
            return Response(
                json.dumps(response),
                headers={"Content-Type": "application/json"},
                status=200
            )

        return Response("Not found", status=404)