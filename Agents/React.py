from typing import Annotated, Sequence, TypedDict
from dotenv import load_dotenv
# The foundational class for all message types in LangGraph
from langchain_core.messages import BaseMessage
# Passes data back to LLM after it calls a tool such as the content and the tool_call_id
from langchain_core.messages import ToolMessage
# Message for providing instructions to the LLM
from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END, START
from langgraph.prebuilt import ToolNode
load_dotenv()


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


@tool
def add(a: int, b: int) -> int:
    """This is an addition function"""
    return a+b


tools = [add]
model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)


def model_call(state: AgentState) -> AgentState:
    system_prompt = SystemMessage(content="You are an AI assistant. answer my query to the best of your ability"
                                  )
    response = model.invoke(
        [system_prompt] + list(state["messages"])
    )
    return {'messages': [response]}


def should_continue(state: AgentState):
    msg = state['messages']
    last_message = msg[-1]
    if not last_message.tool_calls:
        return 'end'
    else:
        return 'continue'


graph = StateGraph(AgentState)

graph.add_node("model", model_call)

tool_node = ToolNode(tools=tools)
graph.add_node('tools', tool_node)

graph.add_edge(START, 'model')
graph.add_conditional_edges(
    'model',
    should_continue,
    {
        'continue': 'tools',
        'end': END,
    }
)

graph.add_edge('tools', 'model')
agent = graph.compile()


def print_stream(stream):
    for s in stream:
        message = s["messages"][-1]
        if isinstance(message, tuple):
            print(message)
        else:
            message.pretty_print()


inputs = {"messages": [("user", "Add 40 + 12")]}
print_stream(agent.stream(inputs, stream_mode="values"))
