from typing import List, Dict,TypedDict
from langgraph.graph import StateGraph,START,END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv



#loading env variables from .env file
load_dotenv()

#Letsts code Agent state schema
class AgentState(TypedDict):
    message: List[HumanMessage]

#lets load llm
llm = ChatOpenAI(model="gpt-4o-mini",temperature=0.9)

#Lets create process node 
def process_node(state: AgentState) -> AgentState:
    #get the last message from the sate
    message = state["message"]
    #invoke llm with the message
    response = llm.invoke(state["message"])
    #print the response eith string like AI: before it
    print(f"AI: {response.content}")
    return state

#Now lets create a graph
app = StateGraph(AgentState)
#add start and end node
app.add_node("process", process_node)
app.add_edge(START, "process")
app.add_edge("process", END)

#lets compile the graph
agent = app.compile()
# lets invoke the graph from user message from console input
user_message = input("User: ")
agent.invoke({"message": [HumanMessage(content=user_message)]})
