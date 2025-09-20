"""
simple bot

1.Define state structure with a list og HumanMessage objects
2.Initialize a GPT-4o model using LangChain's ChatOpenAI
3.Sending and handling different types of messages
4.Building and compiling the graph of the Agent

GOAL:- How to integrate LLM's in out graphs
"""

from typing import TypedDict, List
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

#need add your llm, api key here
class AgentState(TypedDict):
    messages: List[HumanMessage]

def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph=StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

agent=graph.compile()

user_input= input("Enter: ")
while user_input != "exit":
    agent.invoke({"messages": [HumanMessage(content=user_input)]})
    user_input = input("Enter: ")
    