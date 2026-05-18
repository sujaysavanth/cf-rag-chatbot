import uuid
from pyodide.ffi import to_js
from js import Object, Response

def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

async def handle_ingest(data, env):
    text = data.get("text")
    filename = data.get("filename")
    category = data.get("category")
    sub_category = data.get("sub_category")

    if not text:
        return {"status": "error", "message": "missing text"}

    chunks = chunk_text(text)
    file_id = str(uuid.uuid4())

    for index, chunk in enumerate(chunks):
  
        result = await env.AI.run(
            "@cf/baai/bge-base-en-v1.5",
            to_js({"text": [chunk]}, dict_converter=Object.fromEntries)
        )
        
  
        embedding = list(result.data[0].to_py())

        chunk_id = str(uuid.uuid4())
        

        vectorize_payload = to_js([{
            "id": chunk_id,
            "values": embedding,
            "metadata": {"filename": filename, "chunk_index": index}
        }], dict_converter=Object.fromEntries)

        await env.VECTORIZE.upsert(vectorize_payload)


        await env.rag_metadata.prepare(
            "INSERT INTO documents (chunk_id, file_id, chunk_index, text_content, source, category, sub_category) VALUES (?, ?, ?, ?, ?, ?, ?)"
        ).bind(chunk_id, file_id, index, chunk, filename, category, sub_category).run()

    return {"status": "success", "chunks": len(chunks)}

class Worker:
    async def fetch(self, request, env, ctx):
        url = request.url
        if "/ingest" in url and request.method == "POST":
            try:
                data_js = await request.json()
                data = data_js.to_py()
                
                result = await handle_ingest(data, env)
                return Response.json(to_js(result, dict_converter=Object.fromEntries))
            except Exception as e:
                return Response.new(f"Internal Processing Error: {str(e)}", status=500)
                
        return Response.new("Not Found", status=404)

worker = Worker()