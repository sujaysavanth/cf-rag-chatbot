import json
from pyodide.ffi import to_js
from js import Object
from eval import evaluate_response
from urllib.parse import parse_qs

async def handle_query(query_string, env):
    params = parse_qs(query_string)
    query = params.get("question", [""])[0]
    result = await env.AI.run(
        "@cf/baai/bge-base-en-v1.5",
        to_js({"text": [query]}, dict_converter=Object.fromEntries)
    )
    query_embedding = list(result.data[0].to_py())


    search_results = await env.VECTORIZE.query(
        to_js(query_embedding),
        topK=5,
        returnMetadata="all"
    )
    
    chunks = search_results.matches
    context = ""
    

    for match in chunks:
        chunk_id = match.id
        row = await env.rag_metadata.prepare(
            "SELECT text_content FROM documents WHERE chunk_id = ?"
        ).bind(chunk_id).first()
        
        if row and row.text_content:
            context += row.text_content + "\n\n"
    

    system_prompt = """You are an internal company assistant. 
Answer questions ONLY based on the provided context.
If the answer is not in the context, say 'I don't have that information in my knowledge base.'
Do not make up answers."""

    user_prompt = f"""Context:\n{context}\nQuestion: {query}\n\nAnswer:"""
    

    response = await env.AI.run(
        "@cf/meta/llama-3.1-8b-instruct",
        to_js({
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "max_tokens": 500
        }, dict_converter=Object.fromEntries)
    )

    resp_dict = response.to_py()
    
    if "result" in resp_dict:
        answer = resp_dict["result"]["response"]
    else:
        answer = resp_dict.get("response", "No response generated.")


    scores = await evaluate_response(query, context, answer, env)

    return {
        "answer": answer,
        "evaluation": scores,
        "debug": "eval called"
    }