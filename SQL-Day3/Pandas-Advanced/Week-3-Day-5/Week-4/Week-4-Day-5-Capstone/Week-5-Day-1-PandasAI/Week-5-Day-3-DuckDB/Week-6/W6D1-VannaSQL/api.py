
from pathlib import Path
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.encoders import jsonable_encoder

from vanna import Agent
from vanna.core.registry import ToolRegistry
from vanna.core.user import UserResolver, RequestContext, User
from vanna.core.tool.models import ToolContext
from vanna.core.system_prompt.base import SystemPromptBuilder
from vanna.core.system_prompt.default import DefaultSystemPromptBuilder

from vanna.integrations.ollama import OllamaLlmService
from vanna.integrations.sqlite import SqliteRunner
from vanna.integrations.local.agent_memory import DemoAgentMemory

from vanna.tools import RunSqlTool
from vanna.tools.agent_memory import (
    SaveQuestionToolArgsTool,
    SearchSavedCorrectToolUsesTool,
    SaveTextMemoryTool
)


# --------------------------------------------------
# 1. PATH CONFIGURATION
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "job_market.db"


# --------------------------------------------------
# 2. FASTAPI APPLICATION
# --------------------------------------------------

app = FastAPI(
    title="Vanna AI SQL Analyst API",
    description="Text-to-SQL API using Vanna AI, Ollama and SQLite",
    version="1.0.0"
)


# --------------------------------------------------
# 3. REQUEST MODEL
# --------------------------------------------------

class SQLAnalystRequest(BaseModel):
    question: str
    conversation_id: Optional[str] = None


# --------------------------------------------------
# 4. USER RESOLVER
# --------------------------------------------------

class SimpleUserResolver(UserResolver):

    async def resolve_user(self, request_context: RequestContext) -> User:
        return User(
            id="internship_user",
            username="Data Analyst Intern",
            group_memberships=["admin", "user"]
        )


user_resolver = SimpleUserResolver()


# --------------------------------------------------
# 5. OLLAMA LLM CONFIGURATION
# --------------------------------------------------

llm = OllamaLlmService(
    model="qwen2.5:3b",
    host="http://localhost:11434",
    temperature=0.1
)


# --------------------------------------------------
# 6. SQLITE DATABASE CONNECTION
# --------------------------------------------------

if not DB_PATH.exists():
    raise FileNotFoundError(f"Database not found: {DB_PATH}")

sql_runner = SqliteRunner(
    database_path=str(DB_PATH)
)

sql_tool = RunSqlTool(
    sql_runner=sql_runner
)


# --------------------------------------------------
# 7. AGENT MEMORY
# --------------------------------------------------

agent_memory = DemoAgentMemory(max_items=10000)


# --------------------------------------------------
# 8. TOOL REGISTRATION
# --------------------------------------------------

tools = ToolRegistry()

tools.register_local_tool(
    sql_tool,
    access_groups=["admin", "user"]
)

tools.register_local_tool(
    SaveQuestionToolArgsTool(),
    access_groups=["admin"]
)

tools.register_local_tool(
    SearchSavedCorrectToolUsesTool(),
    access_groups=["admin", "user"]
)

tools.register_local_tool(
    SaveTextMemoryTool(),
    access_groups=["admin", "user"]
)


# --------------------------------------------------
# 9. DATABASE SCHEMA PROMPT
# --------------------------------------------------

class JobMarketSystemPromptBuilder(SystemPromptBuilder):

    def __init__(self):
        self.default_builder = DefaultSystemPromptBuilder()

    async def build_system_prompt(self, user, tools) -> Optional[str]:

        base_prompt = await self.default_builder.build_system_prompt(
            user=user,
            tools=tools
        )

        schema_instructions = """
DATABASE SCHEMA INSTRUCTIONS:

Database: job_market.db
Correct table name: job_market

Available columns:
- "Job Title"
- "Location"
- "Salary"
- "Monthly Salary"
- "Locality"
- "State"

STRICT SQL RULES:
1. Always use the exact table name job_market.
2. Never use jobs or jobs_table.
3. Wrap column names containing spaces in double quotes.
4. Use SQLite-compatible SQL syntax.
5. Never invent or assume columns.
6. Always use run_sql for database questions.
7. Pass SQL using the argument name sql.
8. Salary values are in INR. Do not convert or multiply them.
"""

        return f"{base_prompt}\n\n{schema_instructions}"


custom_prompt_builder = JobMarketSystemPromptBuilder()


# --------------------------------------------------
# 10. VANNA AGENT
# --------------------------------------------------

agent = Agent(
    llm_service=llm,
    tool_registry=tools,
    user_resolver=user_resolver,
    agent_memory=agent_memory,
    system_prompt_builder=custom_prompt_builder
)


# --------------------------------------------------
# 11. LOAD FIVE TRAINING EXAMPLES
# --------------------------------------------------

TRAINING_EXAMPLES = [
    (
        "What is the average monthly salary across all job records?",
        'SELECT AVG("Monthly Salary") AS average_monthly_salary FROM job_market;'
    ),
    (
        "Which are the top 10 states by number of job records?",
        "SELECT State, COUNT(*) AS record_count FROM job_market GROUP BY State ORDER BY record_count DESC LIMIT 10;"
    ),
    (
        "Which are the top 10 most common job titles?",
        'SELECT "Job Title", COUNT(*) AS record_count FROM job_market GROUP BY "Job Title" ORDER BY record_count DESC LIMIT 10;'
    ),
    (
        "Which are the top 10 locations with the highest number of job records?",
        "SELECT Location, COUNT(*) AS record_count FROM job_market GROUP BY Location ORDER BY record_count DESC LIMIT 10;"
    ),
    (
        "Which are the top 10 job titles with the highest average monthly salary?",
        'SELECT "Job Title", AVG("Monthly Salary") AS average_monthly_salary FROM job_market GROUP BY "Job Title" ORDER BY average_monthly_salary DESC LIMIT 10;'
    )
]


@app.on_event("startup")
async def load_training_examples():

    api_user = User(
        id="internship_user",
        username="Data Analyst Intern",
        group_memberships=["admin", "user"]
    )

    training_context = ToolContext(
        user=api_user,
        conversation_id=str(uuid.uuid4()),
        request_id=str(uuid.uuid4()),
        agent_memory=agent_memory
    )

    for question, sql in TRAINING_EXAMPLES:

        await agent_memory.save_tool_usage(
            question=question,
            tool_name="run_sql",
            args={"sql": sql},
            context=training_context,
            success=True
        )

    print("Five training examples loaded successfully!")


# --------------------------------------------------
# 12. HEALTH CHECK ENDPOINT
# --------------------------------------------------

@app.get("/")
async def home():

    return {
        "message": "Vanna AI SQL Analyst API is running",
        "database": DB_PATH.name,
        "status": "success"
    }


# --------------------------------------------------
# 13. TEXT-TO-SQL ENDPOINT
# --------------------------------------------------

@app.post("/cia/sql-analyst")
async def sql_analyst(request: SQLAnalystRequest):

    if not request.question.strip():
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )

    try:

        request_context = RequestContext()
        results = []

        async for component in agent.send_message(
            request_context=request_context,
            message=request.question
        ):

            rich = component.rich_component

            if rich is not None:
                results.append(jsonable_encoder(rich))

        return {
            "status": "success",
            "question": request.question,
            "conversation_id": request.conversation_id,
            "results": results
        }

    except Exception as error:

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# --------------------------------------------------
# 14. RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8000
    )
