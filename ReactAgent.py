from typing import TypedDict, Sequence, Annotated
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_core.messages import BaseMessage #the foundational class for all message types in langgraph
from langchain_core.messages import ToolMessage #Passes data back to LLM after it calls a tool such as content
from langchain_core.messages import SystemMessage #To provide instructions to LLM
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph import add_messages
from langgraph.graph import StateGraph,END
from langgraph.prebuilt import ToolNode

#need add your llm, api key here
class AgentState(TypedDict):
  messages: Annotated[Sequence[BaseMessage], add_messages]

@tool
def add(a: int, b: int):
  """Adds a and b."""
  return a + b

@tool
def multiply(a: int, b: int):
  """Multiplies a and b."""
  return a * b

@tool
def subtract(a: int, b: int):
  """Subtracts b from a."""
  return a - b

tools = [add, multiply, subtract]

model = llm.bind_tools(tools)
def model_call(state: AgentState) -> AgentState:
  system_prompt = SystemMessage(content = "You are my AI assistance, please answer my query to the best of you ability.")
  response = model.invoke([system_prompt]+state["messages"])
  return {"messages": [response]}


def should_continue(state: AgentState):
  messages = state["messages"]
  last_message = messages[-1]
  if not last_message.tool_calls:
    return "end"
  else:
    return "continue"

graph = StateGraph(AgentState)
graph.add_node("our_agent", model_call)

tool_node = ToolNode(tools = tools)
graph.add_node("tools", tool_node)

graph.set_entry_point("our_agent")
graph.add_conditional_edges(
  "our_agent",
  should_continue,
  {
    "continue": "tools",
    "end": END
  },
)

graph.add_edge("tools", "our_agent")

app=graph.compile()


def print_stream(stream):
  for s in stream:
    if "messages" in s and s["messages"]:
      message = s["messages"][-1]
      if isinstance(message, tuple):
        print(message)
      else:
        message.pretty_print()

inputs = {"messages": [HumanMessage(content="Add 34 + 21., subtract 12 from 34. multiply 50 by 5, also tel me a joke")]}
print_stream(app.stream(inputs, stream_mode="values"))



#--------------------------------------------------
"""
#Annotated - provides additional context without affecting the type itself

email = Annotated[str, "This has to be a valid email format: "]
print(email.__metadata__)

#Sequence - to autonatically handle the state updates for sequences such as by adding new messages to a chat history

# Reducer Function
# Rule that controls how updates from nodes are combined with the existing state
#Tells us how to merge new data into current state

#without a reducer, updates would have replaced the existing value entirely!

#without a reducer
state={"messages": ["Hi!"]}
updates={"messages": ["Nice to meet you!"]}
new_state={"messages":["Nice to meet you!"]}

#with a reducer
state={"messages": ["Hi!"]}
updates={"messages": ["Nice to meet you!"]}
new_state={"messages":["Hi!","Nice to meet you!"]}
"""

