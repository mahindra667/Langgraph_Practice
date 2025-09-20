"""
1.Use different message types -HumanMessage and Aimessage
2.Maintain a full conversation history using message types
3.Use GPT-4i model using LangChain's ChatOpenAI
4.Create a sophisticated conversation loop

Goal:- Create a form of memory for our Agent
"""
import os
from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END

#need add your llm, api key here

class AgentState(TypedDict):
    messages: List[Union[HumanMessage, AIMessage]]

def process(state: AgentState) -> AgentState:
    """This node will solve the request you input"""
    response = llm.invoke(state["messages"])

    state["messages"].append(AIMessage(content=response.content))
    print(f"\nAI: {response.content}")
    print("Current State: ",state["messages"])
    return state

graph=StateGraph(AgentState)
graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)
agent=graph.compile()

conversation_history = []

user_input = input("Enter: ")
while user_input != "exit":
    conversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({"messages": conversation_history})
    conversation_history = result["messages"]  # Update conversation history with the complete state
    user_input = input("Enter: ")

with open("Agent2_logging.txt", "w") as file:
    file.write("Your conversation log:\n")
    for message in conversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"Human: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n")
        else:
            file.write(f"Unknown message type: {type(message)}\n")
    file.write("\n")
    file.write("End of conversation")
print("Conversation logged to logging.txt")
