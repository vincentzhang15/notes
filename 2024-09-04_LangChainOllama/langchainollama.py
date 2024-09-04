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

MODEL = "llama3.1:405b"
# MODEL = "qwen2:72b-instruct"

async def langchain_ollama():
    from langchain_ollama.llms import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.output_parsers import StrOutputParser

    model = OllamaLLM(model=MODEL)
    prompt = ChatPromptTemplate.from_template("How to make a(n) {item}?")
    parser = StrOutputParser()
    chain = prompt | model | parser

    async for chunk in chain.astream({"item": "apple pie"}):
        print(chunk, end="", flush=True)

def ollama_python():
    import ollama
    model = MODEL
    item = "apple pie"
    messages = [{"role": "user", "content": f"How to make a(n) {item}?"}]
    stream = ollama.chat(model=model, messages=messages, stream=True)
    for chunk in stream:
        print(chunk['message']['content'], end="", flush=True)

if __name__ == "__main__":
    print(" ========================== LangChain + Ollama  ========================== ")
    asyncio.run(langchain_ollama())
    print("\n\n ========================== Ollama Python  ========================== ")
    ollama_python()
    print("\n")
