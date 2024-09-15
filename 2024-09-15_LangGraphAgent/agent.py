"""
2024-09-15
LangGraph agent usage.

References:
https://langchain-ai.github.io/langgraph/#contributing
"""

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode
from langchain_ollama import ChatOllama

from langgraph.graph import END, START, StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.messages import HumanMessage

### Initializations
MODEL = "mistral:7b-instruct"
llm = ChatOllama(model=MODEL, temperature=0)

@tool
def search(query):
    """Surf the web."""
    if "toronto" in query.lower():
        return "It is sunny and 20 degrees Celsius."
    return "It is cloudy and 15 degrees Celsius."

tools = [search]
tool_node = ToolNode(tools=tools)
model = llm.bind_tools(tools)

def call_model(state):
    messages = state['messages']
    response = model.invoke(messages)
    return {"messages": [response]}

def should_continue(state):
    messages = state['messages']
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools" # Go to "tools" node if LLM makes tool call.
    return END

### Define Graph
workflow = StateGraph(MessagesState)
workflow.add_node("agent", call_model) # Cycles between the two nodes.
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent") # agent is the first node called.
workflow.add_conditional_edges("agent", should_continue) # Determine which node to continue to.
workflow.add_edge("tools", "agent") # go to "agent" after "tools" call.

### Run
checkpointer = MemorySaver() # Persist states between graph runs.
app = workflow.compile(checkpointer=checkpointer) # Compile into a LangChain Runnable
final_state = app.invoke(
    {"messages": [HumanMessage(content="what is the weather in toronto? Give the temperature without explanation.")]},
    config={"configurable": {"thread_id": 42}}
)
print(final_state["messages"][-1].content)
