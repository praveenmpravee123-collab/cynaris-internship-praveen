
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from pathlib import Path
import uuid

from vanna import Agent
from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, RequestContext, User
from vanna.core.tool.models import ToolContext
from vanna.core.system_prompt.base import SystemPromptBuilder
from vanna.core.system_prompt.default import DefaultSystemPromptBuilder
from vanna.integrations.local.agent_memory import DemoAgentMemory
from vanna.tools import RunSqlTool


app = FastAPI(
    title="Vanna Sales Assistant API",
    description="Vanna-powered Sales Reporting API",
    version="1.0.0"
)


class QuestionRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


class SimpleUserResolver(UserResolver):
    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="sales_analyst",
            username="Sales Analyst",
            group_memberships=["admin", "user"]
        )


class SalesSystemPromptBuilder(SystemPromptBuilder):
    def __init__(self):
        self.default_builder = DefaultSystemPromptBuilder()

    async def build_system_prompt(self, user, tools):
        base_prompt = await self.default_builder.build_system_prompt(
            user=user,
            tools=tools
        )

        instructions = """
DATABASE: practice.db
TABLE: sales
COLUMNS:
id, product, category, quantity, price, sales_date

RULES:
1. Use only the sales table and listed columns.
2. Use SQLite-compatible SQL.
3. Calculate revenue using quantity * price.
4. Use run_sql for database questions.
5. Never invent columns or tables.
"""
        return f"{base_prompt}\n\n{instructions}"


# Initialize Vanna components
db_path = Path(__file__).parent / "practice.db"

sql_runner = SqliteRunner(database_path=str(db_path))

llm = OllamaLlmService(
    model="qwen2.5:3b",
    host="http://localhost:11434",
    temperature=0.1
)

agent_memory = DemoAgentMemory(max_items=10000)

tools = ToolRegistry()
sql_tool = RunSqlTool(sql_runner=sql_runner)
tools.register_local_tool(sql_tool, access_groups=["admin", "user"])

user_resolver = SimpleUserResolver()
custom_prompt_builder = SalesSystemPromptBuilder()

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    agent_memory=agent_memory,
    system_prompt_builder=custom_prompt_builder
)


@app.get("/")
async def root():
    return {
        "message": "Vanna Sales Assistant API is running",
        "status": "healthy"
    }


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/ask")
async def ask_question(request: QuestionRequest):
    try:
        request_context = RequestContext(
            remote_addr="127.0.0.1"
        )

        conversation_id = request.conversation_id or str(uuid.uuid4())

        results = []

        async for component in agent.send_message(
            request_context=request_context,
            message=request.question,
            conversation_id=conversation_id
        ):
            rich = component.rich_component
            simple = component.simple_component

            item = {
                "type": type(rich).__name__ if rich else None,
                "text": getattr(simple, "text", None) if simple else None
            }

            if rich:
                if hasattr(rich, "content"):
                    item["content"] = rich.content
                if hasattr(rich, "rows"):
                    item["rows"] = rich.rows
                    item["columns"] = rich.columns

            results.append(item)

        return {
            "question": request.question,
            "conversation_id": conversation_id,
            "results": results
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
