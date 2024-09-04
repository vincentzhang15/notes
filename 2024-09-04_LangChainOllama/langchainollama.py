"""
2024-09-04
Comparison of the basic usage of querying an Ollama model
using LangChain and Ollama Python.

>>> References
Chaining with pipes:
https://python.langchain.com/v0.1/docs/expression_language/primitives/sequence/

OllamaLLM:
https://python.langchain.com/v0.2/docs/integrations/llms/ollama/

Streaming output:
https://python.langchain.com/v0.1/docs/expression_language/streaming/

Ollama Python:
https://github.com/ollama/ollama-python
"""

import asyncio

async def langchainollama():
    from langchain_ollama.llms import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    model = OllamaLLM(model="qwen2:72b-instruct")
    prompt = ChatPromptTemplate.from_template("How to make a(n) {item}?")
    parser = StrOutputParser()
    chain = prompt | model | parser

    async for chunk in chain.astream({"item": "apple pie"}):
        print(chunk, flush=True)

def ollama_only():
    import ollama
    model = "qwen2:72b-instruct"
    item = "apple pie"
    messages = [{"role": "user", "content": f"How to make a(n) {item}?"}]
    stream = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in stream:
        print(chunk['message']['content'], end="", flush=True)

if __name__ == "__main__":
    asyncio.run(langchainollama())
    ollama_only()
