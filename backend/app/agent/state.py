from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):
    question: str
    repo_slug: str
    
    messages: Annotated[list, add_messages]     # accumulated msg for next tools
    
    findings: list[dict]                    
    
    proposal: str | None
    

    