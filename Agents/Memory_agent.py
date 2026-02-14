from typing import TypedDict, List, Union
from langchain_core.messages import HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.graph import StateGraph, START, END

load_dotenv()

llm = ChatOpenAI(model='gpt-4o-mini')


class AgentState(TypedDict):
    message: List[Union[HumanMessage, AIMessage]]


def process(state: AgentState) -> AgentState:

    response = llm.invoke(state['message'])
    state['message'].append(AIMessage(content=response.content))
    print(f"AI: {response.content}\n")

    print(f"{state['message']}")
    return state


graph = StateGraph(AgentState)

graph.add_node("process", process)
graph.add_edge(START, "process")
graph.add_edge("process", END)

coversation_history = []

agent = graph.compile()

user_input = input("Enter Message: ")
while user_input != "exit":
    coversation_history.append(HumanMessage(content=user_input))
    result = agent.invoke({'message': coversation_history})

    user_input = input("Enter Message: ")


with open("logging.txt", "w") as file:
    file.write("Your Conversation Log:\n")

    for message in coversation_history:
        if isinstance(message, HumanMessage):
            file.write(f"You: {message.content}\n")
        elif isinstance(message, AIMessage):
            file.write(f"AI: {message.content}\n\n")
    file.write("End of Conversation")

print("Conversation saved to logging.txt")
