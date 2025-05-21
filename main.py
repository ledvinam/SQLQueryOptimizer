import os
import sys
import yaml
from pathlib import Path
from crewai import Agent, Crew, Task
from mcp_client import MCPClient

# --- Agent Definitions using CrewAI ---

def get_athena_agent(schema, sql_code):
    return Agent(
        name="Athena",
        role="SQL Analyst",
        goal="Analyze SQL procedures/functions and database schema to identify optimization opportunities and performance bottlenecks.",
        backstory="Athena is a seasoned database analyst with years of experience in enterprise-scale SQL systems. She has a keen eye for inefficiencies and a deep understanding of query execution plans, always striving to uncover the root causes of slowdowns and suggest actionable improvements.",
        tools=[],
        input={"schema": schema, "sql_code": sql_code}
    )

def get_daedalus_agent(sql_code, recommendations):
    return Agent(
        name="Daedalus",
        role="SQL Writer/Implementor",
        goal="Rewrite and implement optimized SQL code based on the Analyst's recommendations, ensuring best practices and maintainability.",
        backstory="Daedalus is a master SQL developer renowned for crafting high-performance, readable, and robust SQL code. He translates complex optimization strategies into practical, production-ready procedures and functions, always adhering to industry standards.",
        tools=[],
        input={"sql_code": sql_code, "recommendations": recommendations}
    )

def get_hermes_agent(original_sql, optimized_sql, test_queries, db_config, execute_sql_tool):
    return Agent(
        name="Hermes",
        role="SQL Tester",
        goal="Validate the optimized SQL by executing test queries, comparing results, and ensuring data consistency and performance improvements.",
        backstory="Hermes is a meticulous QA engineer specializing in database systems. He designs and runs comprehensive tests to guarantee that optimizations do not alter expected results and that performance targets are met, providing detailed reports for every iteration.",
        tools=[execute_sql_tool],
        input={
            "original_sql": original_sql,
            "optimized_sql": optimized_sql,
            "test_queries": test_queries,
            "db_config": db_config
        }
    )

# --- Utility Functions ---
def load_config(config_path):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

def get_schema_from_mcp(config):
    mcp = MCPClient(config['mcp']['url'], config['mcp'].get('api_key'))
    return mcp.get_schema(config['database']['name'])

def execute_sql_with_mcp(config, sql):
    mcp = MCPClient(config['mcp']['url'], config['mcp'].get('api_key'))
    return mcp.execute_sql(config['database']['name'], sql)

def main():
    if len(sys.argv) < 3 or sys.argv[1] != '--config':
        print("Usage: python main.py --config config.yaml")
        sys.exit(1)
    config_path = sys.argv[2]
    config = load_config(config_path)

    inputs_dir = Path('inputs')
    outputs_dir = Path('outputs')
    outputs_dir.mkdir(exist_ok=True)

    # Load SQL procedure/function and test queries
    sql_files = list(inputs_dir.glob('*.sql'))
    query_files = [f for f in sql_files if 'procedure' not in f.name.lower()]
    proc_files = [f for f in sql_files if 'procedure' in f.name.lower()]
    if not proc_files:
        print("No procedure SQL file found in inputs/.")
        sys.exit(1)
    procedure_path = proc_files[0]
    procedure_sql = read_file(procedure_path)
    test_queries = [read_file(f) for f in query_files]

    # Get schema from MCP
    schema = get_schema_from_mcp(config)

    # --- CrewAI Agents ---
    athena = get_athena_agent(schema, procedure_sql)
    daedalus = get_daedalus_agent(procedure_sql, None)  # Recommendations will be set after Athena's output
    hermes = get_hermes_agent(
        procedure_sql, None, test_queries, config.get('database', {}),
        execute_sql_tool=lambda sql: execute_sql_with_mcp(config, sql)
    )

    # --- CrewAI Tasks ---
    analysis_task = Task(
        description="Analyze the SQL procedure and schema, and generate a list of optimization recommendations.",
        agent=athena
    )
    implementation_task = Task(
        description="Rewrite the SQL procedure according to the recommendations from Athena.",
        agent=daedalus,
        depends_on=[analysis_task]
    )
    testing_task = Task(
        description="Test the optimized SQL using the provided queries and compare results/performance.",
        agent=hermes,
        depends_on=[implementation_task]
    )

    # --- CrewAI Crew (Manager) ---
    crew = Crew(
        name="SQL Optimization Crew",
        tasks=[analysis_task, implementation_task, testing_task]
    )

    # --- Run the CrewAI workflow ---
    results = crew.run()

    # --- Save outputs ---
    analysis_report_path = outputs_dir / 'analysis_report.txt'
    optimized_sql_path = outputs_dir / 'optimized_procedure.sql'
    test_report_path = outputs_dir / 'test_report.txt'

    write_file(analysis_report_path, results[analysis_task])
    write_file(optimized_sql_path, results[implementation_task])
    write_file(test_report_path, results[testing_task])

    print(f"Analysis complete. See {analysis_report_path}")
    print(f"Optimization complete. See {optimized_sql_path}")
    print(f"Testing complete. See {test_report_path}")
    print("\nWorkflow complete. All outputs saved in outputs/ directory.")

if __name__ == '__main__':
    main()
