# SQL Optimization Agents Project (CrewAI Edition)

## Overview
This project implements a robust multi-agent system for SQL query optimization using [CrewAI](https://crewai.com/) for agent orchestration and Model Context Protocol (MCP) for secure MS SQL Server access. The system is implemented in Python and consists of two main agent types:

- **Coordinator (Director) Agent**: Orchestrates the optimization process, reads the database schema, analyzes the procedure, generates a step-by-step plan, and manages the workflow using CrewAI's agent management capabilities.
- **Worker Agent**: Receives a single optimization step and the current procedure SQL, applies the step using LLMs (OpenAI or other), and returns the optimized SQL.

## Architecture

### Agents (CrewAI)

#### Coordinator Agent
- Uses CrewAI to manage and coordinate Worker Agents.
- Reads the database schema from the target MS SQL database.
- Analyzes the stored procedure and generates a step-by-step optimization plan using the schema and LLM.
- Executes the provided query and stores the result for later comparison.
- For each step in the plan:
  - Spawns a new Worker Agent via CrewAI, passing the current procedure SQL and the step instruction (plus any error feedback if needed).
  - Deploys and validates the result after each step, retrying up to 5 times if needed.
  - Only proceeds to the next step if the current one is valid (deploys and produces correct results).
- After all steps, deploys and validates the final optimized procedure.
- Stores all intermediate/final SQLs, results, and errors for traceability.

#### Worker Agent
- Receives a single optimization step and the current procedure SQL (plus any error feedback) from the Coordinator via CrewAI.
- Uses an LLM (OpenAI or other) to rewrite the procedure according to the step and feedback.
- Returns the optimized SQL to the Coordinator Agent.

### Communication Flow (CrewAI)
1. **Coordinator**: Reads schema, analyzes procedure, generates plan.
2. **Coordinator**: Executes original query, stores result.
3. **Coordinator → Worker (via CrewAI)**: For each step, spawns a Worker Agent and requests optimization, passing current SQL and step instruction (plus error feedback if needed).
4. **Coordinator**: Deploys and validates each step, retries up to 5 times if needed.
5. **Coordinator**: If all steps succeed, deploys and validates final procedure.
6. **Coordinator**: Compares results and performance, iterates if needed.

### Technologies
- **CrewAI**: For agent orchestration and message passing.
- **Model Context Protocol (MCP)**: For secure, programmatic access to MS SQL Server.
- **Python**: For agent implementation.
- **MS SQL Server**: Target database for optimization.

## Usage

Run the app with:
```
python main.py <query-sql-file-1> <query-sql-file-2> ... <procedure-sql-file>
```

- You can provide a list of query SQL files to increase the number of data result samples for comparison.
- All intermediate/final SQLs, results, and errors are saved for each step and iteration.
- Requires the `OPENAI_API_KEY` environment variable and a running MCP server.
- CrewAI must be configured and running to enable agent orchestration.

## Example Output Files
- `procedure.sql.step01.try01.sql` — SQL after step 1, first attempt
- `procedure.sql.step01.try01.rpt` — Result of executing the query after step 1, first attempt
- `procedure.sql.step01.try01.err` — Error (if any) for step 1, first attempt
- `procedure.sql.final.sql` — Final SQL after all steps
- `procedure.sql.final.rpt` — Final result after all steps

## Key Features
- Multi-agent, message-passing architecture powered by CrewAI
- Schema-aware, stepwise optimization with retries and error feedback
- Full traceability of all changes and results

## References
- [CrewAI](https://crewai.com/)
- [CrewAI Docs](https://docs.crewai.com/)]
- [MCP MSSQL](https://github.com/dperussina/mssql-mcp-server)
