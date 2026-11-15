
from pathlib import Path
from uuid import uuid4
from typing import Optional

from fastapi import HTTPException
from pydantic import BaseModel

from vanna import Agent, Tool
from vanna.core.tool.models import ToolResult
from vanna.capabilities.sql_runner.models import RunSqlToolArgs
from vanna.integrations.sqlite import SqliteRunner
from vanna.core.registry import ToolRegistry
from vanna.integrations.local.agent_memory.in_memory import DemoAgentMemory
from vanna.integrations.local import MemoryConversationStore
from vanna.core.user.resolver import UserResolver
from vanna.core.user.request_context import RequestContext
from vanna.core.user.models import User
from vanna import AgentConfig
from vanna.core.system_prompt.default import DefaultSystemPromptBuilder
from vanna.integrations.ollama import OllamaLlmService

from vanna.servers.fastapi import VannaFastAPIServer
from vanna.servers.base.models import ChatRequest


# 1. Database Setup
BASE_DIR = Path(__file__).resolve().parent
db_path = str(BASE_DIR / "crm_database.db")

sql_runner = SqliteRunner(database_path=db_path)


# 2. CRM SQL Tool
class CRMQueryTool(Tool):

    @property
    def name(self) -> str:
        return "run_sql"

    @property
    def description(self) -> str:
        return "Execute read-only SQL queries on the CRM customers database."

    def get_args_schema(self):
        return RunSqlToolArgs

    async def execute(self, context, args: RunSqlToolArgs) -> ToolResult:
        try:
            result = await sql_runner.run_sql(args, context)

            return ToolResult(
                success=True,
                result_for_llm=result.to_string(index=False)
            )

        except Exception as e:
            return ToolResult(
                success=False,
                result_for_llm=f"SQL execution failed: {e}",
                error=str(e)
            )


crm_sql_tool = CRMQueryTool()


# 3. Tool Registry
tool_registry = ToolRegistry()

tool_registry.register_local_tool(
    crm_sql_tool,
    access_groups=["admin", "user"]
)


# 4. Agent Memory
agent_memory = DemoAgentMemory(max_items=1000)


# 5. Conversation Store
conversation_store = MemoryConversationStore()


# 6. User Resolver
class LocalUserResolver(UserResolver):

    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="crm_user_001",
            username="CRM Analyst",
            group_memberships=["user"]
        )


user_resolver = LocalUserResolver()


# 7. CRM System Prompt
crm_system_prompt = """
You are an expert CRM Data Analyst and SQL Assistant.

DATABASE:
- SQLite database
- Table name: customers

TABLE SCHEMA:
1. customer_id TEXT
2. customer_name TEXT
3. company TEXT
4. lead_source TEXT
5. sales_rep TEXT
6. deal_value INTEGER
7. deal_stage TEXT
8. status TEXT
9. created_date TIMESTAMP
10. last_activity TIMESTAMP

INSTRUCTIONS:
- Answer CRM questions using SQL queries.
- Use the available run_sql tool to execute SQL.
- Never claim that you cannot access the database.
- Generate valid SQLite SQL syntax.
- Use only the customers table and its listed columns.
- For customer counts, use COUNT(*).
- For deal value totals, use SUM(deal_value).
- Display monetary values in Indian Rupees (INR).
- Do not modify or delete database records.
- Never invent query results.
- Summarize the actual SQL results clearly.
"""

crm_prompt_builder = DefaultSystemPromptBuilder(
    base_prompt=crm_system_prompt
)


# 8. Ollama LLM
ollama_llm = OllamaLlmService(
    model="qwen2.5:3b",
    host="http://localhost:11434",
    timeout=240.0,
    num_ctx=8192,
    temperature=0.1
)


# 9. Agent Configuration
agent_config = AgentConfig(
    max_tool_iterations=5,
    stream_responses=False,
    temperature=0.0
)


# 10. Initialize CRM Agent
agent = Agent(
    llm_service=ollama_llm,
    tool_registry=tool_registry,
    user_resolver=user_resolver,
    agent_memory=agent_memory,
    conversation_store=conversation_store,
    config=agent_config,
    system_prompt_builder=crm_prompt_builder
)


# 11. Initialize Vanna FastAPI Server
vanna_server = VannaFastAPIServer(agent=agent)
app = vanna_server.create_app()


# 12. API Request Model
class SQLAnalystRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


# 13. CRM SQL Analyst Endpoint
@app.post("/cia/sql-analyst")
async def sql_analyst(request: SQLAnalystRequest):

    try:
        chat_request = ChatRequest(
            message=request.question,
            conversation_id=request.conversation_id or str(uuid4()),
            metadata={}
        )

        chat_response = await vanna_server.chat_handler.handle_poll(
            chat_request
        )

        answers = []

        for chunk in chat_response.chunks:
            if chunk.simple:
                answers.append(chunk.simple)

        return {
            "success": True,
            "conversation_id": chat_response.conversation_id,
            "request_id": chat_response.request_id,
            "answer": answers
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


print("CRM SQL Analyst API initialized successfully!")
print("Database:", db_path)
print("LLM: qwen2.5:3b")
print("Endpoint: POST /cia/sql-analyst")
