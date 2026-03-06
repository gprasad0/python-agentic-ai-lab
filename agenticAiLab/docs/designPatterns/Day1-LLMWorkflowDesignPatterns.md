LLM WORKFLOW DESIGN PATTERNS

1. # PROMPT CHAINING
   its just a chaining of LLMS that finally gives an output. There can be a code block in between but its a simple chaining
   Prompt chaining is simply a sequential pipeline of multiple LLM calls.
   A code block can exist between steps, but the flow is strictly linear.

```
input -> llm1 -> llm2 -> (code block) -> llm3 -> output
```

2. ROUTING
   for a given input , there is a LLM router that routes the action or input to various other specialized llms. The LLM router has the autonomy of selecting which LLM should perform the tasks . SO only a single LLM is selected for its specialized subtasks.

```
                    -> SPECIALIZED LLM 1
input -> LLMROUTER  -> SPECIALIZED LLM 2 -> output
                    -> SPECIALIZED LLM 3
```

3. # PARALLELIZATION
   This will have a code block that sperates the tasks into multiple sections and feeds it to multiple LLMS that work parallely. These LLMS then give their outputs to another code block that stitches all the LLM outputs into single result and spits it out - This is concurrently running the LLMS

```
                                -> LLM1 ->
input -> CodeBlock/Co-ordinator -> LLM2 -> -> CodeBlock/Aggregator -> output
                                -> LLM3 ->
```

4. # ORCHESTRATOR-WORKER
   This is similar to the PARALLELIZATION workflow pattern but instaed of the codeblock there is a LLM that decides what subtasks should go to which LLM. Later there is a LLM that stitches together all the results from the LLMS and gives an output
   Complex tasks are broken down dynamically and combined

```
                          -> LLM1 ->
input -> LLM/Orchestrator -> LLM2 -> -> LLM/synthesizer -> output
                          -> LLM3 ->
```

5. # EVALUATOR - OPTIMIZER
   This is basically a feedback loop . An iput comes in, the LLM takes it and processes it. Then the LLMS output is given to a different LLM for feedback and evaluate the results. It can either take it as correct/accepts and gives the output or sends it back with a rejection and a reason to the earlier LLM .

```
            solution
              ->
input -> LLMl     LLM2 -> output
              <-
    Rejected with feedback
```

# Multi-Agent Architecture Patterns

When building AI systems with the OpenAI Agents SDK (or similar frameworks), there are several common design patterns for coordinating multiple agents.

The three most common patterns are:

1. **Agent-as-Tool Pattern**
2. **Handoff Pattern**
3. **Orchestrator Pattern**

Understanding these patterns helps you design **scalable and maintainable multi-agent systems**.

---

# 1. Agent-as-Tool Pattern

## Overview

In this pattern, **an agent is exposed as a tool** that another agent can call.

The main agent stays in control of the conversation and simply **invokes other agents as tools** when needed.

This is useful when you want **specialized capabilities but centralized control**.

---

## Architecture

```
User
 ↓
Main Agent
 ↓
Agent Tool (Specialist Agent)
 ↓
Tool Result
 ↓
Main Agent Responds
```

---

## Example

### Specialist Agent

```python
from agents import Agent

math_agent = Agent(
    name="math_agent",
    instructions="Solve math problems"
)
```

### Convert Agent to Tool

```python
math_tool = math_agent.as_tool(
    tool_name="math_solver",
    tool_description="Solve mathematical problems"
)
```

### Main Agent

```python
main_agent = Agent(
    name="assistant",
    instructions="Help the user with different tasks",
    tools=[math_tool]
)
```

---

## Flow

User prompt:

```
What is 25 * 14?
```

Flow:

```
User
 ↓
Main Agent
 ↓
Calls math_solver tool
 ↓
Math Agent calculates result
 ↓
Main Agent returns answer
```

The **main agent remains in control**.

---

## When to Use

Use Agent-as-Tool when:

- You want **centralized control**
- You need **specialized capabilities**
- You want a **single agent managing the conversation**

Common examples:

- Code generation agent
- Math solving agent
- Data analysis agent

---

# 2. Handoff Pattern

## Overview

In the **handoff pattern**, the current agent **transfers the conversation to another agent**.

The new agent **takes control of the conversation**.

This is similar to how customer support systems transfer calls between departments.

---

## Architecture

```
User
 ↓
Router Agent
 ↓
Handoff
 ↓
Specialist Agent
 ↓
User Response
```

---

## Example

### Specialist Agents

```python
travel_agent = Agent(
    name="travel_agent",
    instructions="Help with travel planning"
)

coding_agent = Agent(
    name="coding_agent",
    instructions="Help with programming problems"
)
```

### Router Agent

```python
router_agent = Agent(
    name="router",
    instructions="Route the user to the correct specialist",
    handoffs=[travel_agent, coding_agent]
)
```

---

## Flow

User prompt:

```
Help me debug my Python code
```

Flow:

```
User
 ↓
Router Agent
 ↓
Handoff to Coding Agent
 ↓
Coding Agent handles the conversation
```

The **router agent stops controlling the conversation**.

---

## When to Use

Use handoffs when:

- You have **multiple specialist agents**
- Each agent owns a **specific domain**
- You want **domain-specific conversations**

Examples:

- Travel assistant
- Coding assistant
- Financial advisor
- Customer support routing

---

# 3. Orchestrator Pattern

## Overview

The **orchestrator pattern** is used when a central agent **coordinates multiple agents and tasks** to solve a complex problem.

Unlike tools or handoffs, the orchestrator can:

- Plan tasks
- Call multiple agents
- Combine results
- Produce a final answer

This pattern is common in **complex AI workflows**.

---

## Architecture

```
User
 ↓
Orchestrator Agent
 ↓
Task Planning
 ↓
Specialist Agents
 ↓
Combine Results
 ↓
Final Answer
```

---

## Example Workflow

Example task:

```
Research Tesla stock and summarize whether it is a good investment.
```

Flow:

```
User
 ↓
Orchestrator Agent
 ↓
Call Research Agent
 ↓
Call Financial Analysis Agent
 ↓
Call Summarization Agent
 ↓
Final Combined Answer
```

---

## Example Conceptual Code

```python
research_agent = Agent(
    name="research_agent",
    instructions="Find information about companies"
)

analysis_agent = Agent(
    name="analysis_agent",
    instructions="Analyze financial data"
)

summary_agent = Agent(
    name="summary_agent",
    instructions="Summarize complex information"
)
```

The orchestrator decides:

1. Which agent to call
2. In what order
3. How to combine the results

---

## When to Use

Use the orchestrator pattern when:

- Tasks require **multiple steps**
- You need **task decomposition**
- Results must be **combined from multiple agents**

Examples:

- Market research
- Data analysis pipelines
- Multi-step reasoning tasks
- AI workflow automation

---

# Comparison

| Feature            | Agent-as-Tool               | Handoff               | Orchestrator                           |
| ------------------ | --------------------------- | --------------------- | -------------------------------------- |
| Control            | Main agent stays in control | Control transferred   | Central orchestrator controls workflow |
| Purpose            | Use specialist capability   | Transfer conversation | Coordinate multiple tasks              |
| Conversation owner | Main agent                  | New agent             | Orchestrator                           |
| Typical complexity | Low                         | Medium                | High                                   |

---

# Mental Model

You can think of these patterns like a workplace:

**Agent-as-Tool**

Manager asks a specialist to perform a task.

```
Manager → Accountant → Result → Manager responds
```

**Handoff**

Manager transfers the customer to another department.

```
Customer → Reception → Transfer → Specialist
```

**Orchestrator**

Project manager coordinates multiple teams.

```
Project Manager
 ↓
Research Team
 ↓
Analysis Team
 ↓
Report Team
```

---

# Production Systems

Most real-world AI systems combine these patterns:

```
User
 ↓
Router Agent
 ↓
Specialist Agents (handoffs)
 ↓
Each Agent Uses Tools
 ↓
Orchestrator Combines Results
```

---

# Summary

Agent-as-Tool → Use another agent as a capability
Handoff → Transfer conversation control to another agent
Orchestrator → Coordinate multiple agents to solve complex tasks

Choosing the correct pattern depends on the **complexity of the system and task requirements**.
