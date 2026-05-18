import json
from pyodide.ffi import to_js
from js import Object

def to_js_obj(x):
    return to_js(x, dict_converter=Object.fromEntries)

async def evaluate_response(question, context, answer, env):
    eval_prompt = f"""You are an expert evaluator for a RAG system.
Score the following response on two criteria, respond in JSON only:

Question: {question}
Context: {context}
Answer: {answer}

Evaluate and return ONLY this JSON:
{{
    "relevance_score": <1-10>,
    "faithfulness_score": <1-10>,
    "reasoning": "<one sentence why>"
}}"""


    response = await env.AI.run(
        "@cf/meta/llama-3.1-8b-instruct",
        to_js_obj({
            "messages": [
                {"role": "system", "content": "You are an evaluation assistant. Always respond with valid JSON only, no extra text or explanations outside the JSON."},
                {"role": "user", "content": eval_prompt}
            ],
            "max_tokens": 300
        })
    )


    resp_dict = response.to_py()
    
    if "result" in resp_dict:
        raw_text = resp_dict["result"]["response"]
    else:
        raw_text = resp_dict.get("response", "")


    cleaned_text = raw_text.strip()
    if cleaned_text.startswith("```"):
        # Remove opening ```json or ```
        cleaned_text = cleaned_text.split("\n", 1)[-1]
        # Remove closing ```
        if cleaned_text.endswith("```"):
            cleaned_text = cleaned_text.rsplit("```", 1)[0]
        cleaned_text = cleaned_text.strip()


    try:
        scores = json.loads(cleaned_text)
    except Exception as e:
        scores = {
            "relevance_score": -1,
            "faithfulness_score": -1,
            "reasoning": f"Failed to parse eval response. Raw output was: {raw_text[:100]}"
        }

    return scores