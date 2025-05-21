# SQL Optimization Agents Project (CrewAI Edition)

## Overview
This project implements a robust multi-agent system for SQL query optimization using [CrewAI](https://crewai.com/) for agent orchestration and Model Context Protocol (MCP) for secure MS SQL Server access. The system is implemented in Python and leverages CrewAI's native Manager agent to coordinate three specialized agents:

### CrewAI Agents

#### 1. SQL Analyst
- **Name:** Athena
- **Goal:** Analyze SQL procedures/functions and database schema to identify optimization opportunities and performance bottlenecks.
- **Backstory:** Athena is a seasoned database analyst with years of experience in enterprise-scale SQL systems. She has a keen eye for inefficiencies and a deep understanding of query execution plans, always striving to uncover the root causes of slowdowns and suggest actionable improvements.

#### 2. SQL Writer/Implementor
- **Name:** Daedalus
- **Goal:** Rewrite and implement optimized SQL code based on the Analyst's recommendations, ensuring best practices and maintainability.
- **Backstory:** Daedalus is a master SQL developer renowned for crafting high-performance, readable, and robust SQL code. He translates complex optimization strategies into practical, production-ready procedures and functions, always adhering to industry standards.

#### 3. SQL Tester
- **Name:** Hermes
- **Goal:** Validate the optimized SQL by executing test queries, comparing results, and ensuring data consistency and performance improvements.
- **Backstory:** Hermes is a meticulous QA engineer specializing in database systems. He designs and runs comprehensive tests to guarantee that optimizations do not alter expected results and that performance targets are met, providing detailed reports for every iteration.

The CrewAI Manager agent (native to CrewAI) orchestrates the workflow between these agents, ensuring a seamless, iterative optimization process.

## Architecture & Workflow

### Agents (CrewAI)
- **Manager Agent (CrewAI native):** Orchestrates the workflow between Athena (Analyst), Daedalus (Writer), and Hermes (Tester).
- **Athena (Analyst):** Analyzes input SQL and schema, produces optimization recommendations.
- **Daedalus (Writer):** Implements the recommended optimizations in the SQL code.
- **Hermes (Tester):** Validates the optimized SQL against provided queries and expected results.

### Communication & File Flow
1. **Input:**
   - Place your SQL procedures/functions in the `inputs/` directory.
   - Place your test queries in the same directory or as specified.
   - Update `config.yaml` with your database connection details.
2. **Analysis:**
   - Athena reviews the SQL and schema, generating a list of optimization steps and rationale.
   - Output: `outputs/analysis_report.txt` (recommendations and identified issues).
3. **Implementation:**
   - Daedalus rewrites the SQL according to Athena's recommendations.
   - Output: `outputs/optimized_procedure.sql` (optimized SQL code).
4. **Testing:**
   - Hermes executes the provided queries against both the original and optimized SQL, comparing results and performance.
   - Output: `outputs/test_report.txt` (data consistency and performance comparison).
5. **Iteration:**
   - The Manager agent coordinates further iterations if issues are found, until all agents agree on the final optimized solution.
6. **Final Output:**
   - All intermediate and final files (analysis, optimized SQL, test reports) are saved in the `outputs/` directory for traceability.

## Technologies
- **CrewAI:** For agent orchestration and message passing.
- **Model Context Protocol (MCP):** For secure, programmatic access to MS SQL Server.
- **Python:** For agent implementation.
- **MS SQL Server:** Target database for optimization.

## Usage

Run the app with:
```
python main.py --config config.yaml
```

- Place your SQL procedures/functions and test queries in `inputs/`.
- All intermediate/final SQLs, analysis, and test reports are saved in `outputs/`.
- Requires the `OPENAI_API_KEY` environment variable and a running MCP server.
- CrewAI must be configured and running to enable agent orchestration.

## Example Output Files
- `outputs/analysis_report.txt` — Analyst's recommendations and findings
- `outputs/optimized_procedure.sql` — Optimized SQL after implementation
- `outputs/test_report.txt` — Test results and performance comparison

## Key Features
- Multi-agent, message-passing architecture powered by CrewAI's native Manager
- Professional-grade SQL analysis, implementation, and testing
- Schema-aware, stepwise optimization with full traceability

## References
- [CrewAI](https://crewai.com/)
- [CrewAI Docs](https://docs.crewai.com/)
- [MCP MSSQL](https://github.com/dperussina/mssql-mcp-server)
