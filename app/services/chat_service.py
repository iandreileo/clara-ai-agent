from fastapi import HTTPException
from typing import Dict, Optional
from typing_extensions import Annotated
from uuid import uuid4

from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.tools.resume_tools import resume_tools
from app.api.v1.models import ChatResponse, ChatHistory

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from typing import Annotated

from langchain_openai import ChatOpenAI
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from langchain_core.runnables import RunnableConfig
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import ToolMessage

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

DB_URI = settings.DB_URI

def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state["messages"][-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {repr(error)}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }

def create_tool_node_with_fallback(tools: list) -> dict:
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)], exception_key="error"
    )



class State(TypedDict):
    messages: Annotated[list, add_messages]

class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: State, config: RunnableConfig):
        while True:
            configuration = config.get("configurable", {})
            user_token = configuration.get("user_token", None)
            state = {**state, "user_token": user_token}
            result = await self.runnable.ainvoke(state)
            # If the LLM happens to return an empty response, we will re-prompt it
            # for an actual response.
            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state["messages"] + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}
    


class ChatService:
    def __init__(self):
        self.conversations: Dict[str, Dict] = {}
        self.llm = ChatOpenAI(model=settings.OPENAI_MODEL)
        self.tools = resume_tools
        # Create the prompt template
        self.prompt = ChatPromptTemplate.from_messages([
            (
                "system",
                "You are Clara - an AI assistant that helps users build their resume. "
                "You will answer only on questions related to the resume.\n"
                "You need to fill each section of the resume one by one.\n"
                "You will use the available tools to send a section of the resume to the server.\n"
                "You will not use the same tool more than once.\n"
                "You will not ask the user to fill the same section more than once.\n"
                "You will always ask the user to fill the next missing section of the resume.\n"
                "Confirm with the user before saving each section.\n"
                "Sections are " + ", ".join([section for section in settings.RESUME_SECTIONS]) + ".\n"
            ),
            ("placeholder", "{messages}")
        ])

        # Create the assistant runnable
        assistant_runnable = self.prompt | self.llm.bind_tools(self.tools)

        # Build the graph
        self.builder = StateGraph(State)
        self.builder.add_node("assistant", Assistant(assistant_runnable))
        self.builder.add_node("tools", create_tool_node_with_fallback(self.tools))
        
        # Define edges
        self.builder.add_edge(START, "assistant")
        self.builder.add_conditional_edges(
            "assistant",
            tools_condition,
        )
        self.builder.add_edge("tools", "assistant")


    async def process_message(self, 
                            message: str, 
                            user_token: str,
                            conversation_id: Optional[str] = str(uuid4())) -> ChatResponse:
        """Process a chat message and return the response"""
        try:
            # Create config for this invocation
            config = {
                "configurable": {
                    "thread_id": conversation_id,
                    "user_token": user_token,
                },
                
            }
            
            async with AsyncPostgresSaver.from_conn_string(DB_URI) as checkpointer:
                await checkpointer.setup()    

                graph = self.builder.compile(checkpointer=checkpointer)

                # Get response from agent
                response = await graph.ainvoke({"messages": [("user", message)]}, config)

                # Extract the final answer from the response
                # LangGraph agents return the last message in the messages list
                final_response = response["messages"][-1].content
                
                return ChatResponse(
                    response=final_response,
                    conversation_id=conversation_id,
                )
            
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail=str(e))
