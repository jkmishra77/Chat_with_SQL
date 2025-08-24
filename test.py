# backend.py

from crewai import Agent, Task, Crew, Process
from crewai.tools import tool
import sqlite3
from typing import List, Tuple
from llm.llm import setup_llm

# ---------------------- TOOL DEFINITION ----------------------

@tool("sql_execution_tool")
def sql_execution_tool(sql_query: str, db_path: str = "student.db") -> List[Tuple]:
    """Executes SELECT SQL queries on SQLite database and returns results."""
    try:
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        conn.commit()
        conn.close()
        return rows
    except sqlite3.OperationalError as e:
        return [(f"SQL Error: {e}",)]
    except Exception as e:
        return [(f"Unexpected Error: {e}",)]

# ---------------------- AGENT DEFINITIONS ----------------------

llm = setup_llm()

sql_generation_agent = Agent(
    role='SQL Query Generator',
    goal='Convert natural language questions to precise SQLite SELECT queries',
    backstory="""Expert SQL developer specializing in converting English questions 
    to efficient SQL queries for student database. Returns only clean SQL code.""",
    verbose=True,
    llm=llm
)

sql_execution_agent = Agent(
    role='SQL Query Executor',
    goal='Execute SQL queries on database and return results',
    backstory="""Database operations specialist who executes SQL queries 
    and handles database connections efficiently.""",
    tools=[sql_execution_tool],
    verbose=True
)

# ---------------------- TASK DEFINITIONS ----------------------

def sql_generation_task(question: str) -> Task:
    return Task(
        description=(
            "Convert the following English question into a valid SQLite SELECT query. "
            "Use the STUDENT database with columns: NAME, CLASS, SECTION, MARKS. "
            "Do not include explanations, formatting, or comments — return only the SQL query. "
            f"Question: {question}"
        ),
        expected_output="A syntactically correct SQLite SELECT query.",
        agent=sql_generation_agent
    )

def sql_execution_task(sql_query: str, context_task: Task) -> Task:
    return Task(
        description=(
            "Execute the following SQL query on the STUDENT database. "
            "Return the query results in a clean, readable format. "
            f"SQL Query: {sql_query}"
        ),
        expected_output="Formatted query results from the database.",
        agent=sql_execution_agent,
        context=[context_task]
    )

# ---------------------- CREW ORCHESTRATION ----------------------

class SQLBackend:
    def __init__(self):
        pass

    def process_question(self, question: str) -> dict:
        # Step 1: Create tasks
        gen_task = sql_generation_task(question)
        exec_task = sql_execution_task(sql_query="{task.output}", context_task=gen_task)

        # Step 2: Assemble crew
        crew = Crew(
            agents=[sql_generation_agent, sql_execution_agent],
            tasks=[gen_task, exec_task],
            process=Process.sequential
        )

        # Step 3: Execute
        result = crew.kickoff(inputs={"question": question})

        return {
            "question": question,
            "sql_query": result[0].raw.strip(),
            "results": result[1].raw
        }

# ---------------------- CLI TEST ----------------------

if __name__ == "__main__":
    backend = SQLBackend()
    question = "Show students with marks greater than 90"
    output = backend.process_question(question)

    print("🔍 Question:", output["question"])
    print("🧠 Generated SQL:\n", output["sql_query"])
    print("📊 Results:\n", output["results"])
