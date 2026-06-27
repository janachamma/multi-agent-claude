"""
Multi-Agent AI System using Anthropic Claude API
Author: Jana Chamma
Description: A multi-agent system where specialized AI agents collaborate
             to answer complex questions through task decomposition and reasoning.
"""

import anthropic
import json
from datetime import datetime

# Initialize Anthropic client
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
MODEL = "claude-sonnet-4-6"

# =============================================================================
# AGENT DEFINITIONS
# Each agent has a specific role and system prompt
# =============================================================================

AGENTS = {
    "coordinator": {
        "name": "Coordinator Agent",
        "role": "Break down complex questions into subtasks and assign them to specialist agents.",
        "system": """You are a Coordinator Agent in a multi-agent AI system.
Your job is to:
1. Analyze the user's question
2. Break it into 2-3 clear subtasks
3. Assign each subtask to the right specialist: 'researcher', 'analyst', or 'writer'

Respond ONLY in this JSON format:
{
  "subtasks": [
    {"agent": "researcher", "task": "..."},
    {"agent": "analyst", "task": "..."},
    {"agent": "writer", "task": "..."}
  ]
}"""
    },
    "researcher": {
        "name": "Researcher Agent",
        "role": "Gather and summarize relevant facts and information.",
        "system": """You are a Researcher Agent in a multi-agent AI system.
Your job is to gather relevant facts, background information, and key points about the given topic.
Be thorough, factual, and organized. Present information in clear bullet points."""
    },
    "analyst": {
        "name": "Analyst Agent",
        "role": "Analyze information, identify patterns, and draw insights.",
        "system": """You are an Analyst Agent in a multi-agent AI system.
Your job is to analyze the topic critically, identify patterns, evaluate trade-offs,
and provide data-driven insights. Think deeply and provide structured analysis."""
    },
    "writer": {
        "name": "Writer Agent",
        "role": "Synthesize all information into a clear, well-structured final answer.",
        "system": """You are a Writer Agent in a multi-agent AI system.
Your job is to take research and analysis from other agents and synthesize it into
a clear, well-structured, and comprehensive final answer for the user.
Make it readable, organized, and actionable."""
    }
}


# =============================================================================
# CORE AGENT FUNCTION
# =============================================================================

def run_agent(agent_key: str, task: str, context: str = "") -> str:
    """Run a single agent on a given task."""
    agent = AGENTS[agent_key]
    
    user_message = task
    if context:
        user_message = f"Context from previous agents:\n{context}\n\nYour task: {task}"
    
    print(f"\n🤖 [{agent['name']}] Working on: {task[:80]}...")
    
    response = client.messages.create(
        model=MODEL,
        max_tokens=1000,
        system=agent["system"],
        messages=[{"role": "user", "content": user_message}]
    )
    
    result = response.content[0].text
    print(f"✅ [{agent['name']}] Done.")
    return result


# =============================================================================
# MULTI-AGENT PIPELINE
# =============================================================================

def run_multi_agent_pipeline(user_question: str) -> dict:
    """
    Run the full multi-agent pipeline:
    1. Coordinator breaks down the question
    2. Specialist agents work on subtasks
    3. Writer synthesizes the final answer
    """
    print("\n" + "="*60)
    print("MULTI-AGENT AI PIPELINE")
    print("="*60)
    print(f"📝 Question: {user_question}")
    print("="*60)
    
    results = {}
    
    # --- STEP 1: Coordinator decomposes the task ---
    print("\n📋 STEP 1: Coordinator analyzing question...")
    coordinator_output = run_agent("coordinator", user_question)
    
    try:
        plan = json.loads(coordinator_output)
        subtasks = plan["subtasks"]
        print(f"\n📌 Plan: {len(subtasks)} subtasks identified")
        for i, subtask in enumerate(subtasks, 1):
            print(f"   {i}. [{subtask['agent'].upper()}] {subtask['task'][:60]}...")
    except json.JSONDecodeError:
        # Fallback if coordinator doesn't return valid JSON
        subtasks = [
            {"agent": "researcher", "task": user_question},
            {"agent": "analyst", "task": f"Analyze: {user_question}"},
            {"agent": "writer", "task": f"Summarize findings about: {user_question}"}
        ]
    
    results["coordinator"] = coordinator_output
    
    # --- STEP 2: Specialist agents work on subtasks ---
    specialist_outputs = []
    
    for subtask in subtasks:
        agent_key = subtask["agent"]
        if agent_key in ["researcher", "analyst"]:
            output = run_agent(agent_key, subtask["task"])
            results[agent_key] = output
            specialist_outputs.append(f"[{AGENTS[agent_key]['name']}]:\n{output}")
    
    # --- STEP 3: Writer synthesizes final answer ---
    print("\n✍️  STEP 3: Writer synthesizing final answer...")
    context = "\n\n".join(specialist_outputs)
    
    writer_task = f"Write a comprehensive answer to this question: '{user_question}'"
    final_answer = run_agent("writer", writer_task, context)
    results["writer"] = final_answer
    results["final_answer"] = final_answer
    
    return results


# =============================================================================
# INTERACTIVE CHAT LOOP
# =============================================================================

def main():
    print("\n" + "="*60)
    print("🧠 MULTI-AGENT AI ASSISTANT")
    print("Powered by Anthropic Claude")
    print("Author: Jana Chamma")
    print("="*60)
    print("Type your question and watch multiple AI agents collaborate!")
    print("Type 'quit' to exit\n")
    
    conversation_log = []
    
    while True:
        user_input = input("\n💬 Your question: ").strip()
        
        if user_input.lower() in ["quit", "exit", "q"]:
            print("\n👋 Goodbye! Agents signing off.")
            break
        
        if not user_input:
            print("Please enter a question.")
            continue
        
        start_time = datetime.now()
        
        # Run the multi-agent pipeline
        results = run_multi_agent_pipeline(user_input)
        
        end_time = datetime.now()
        duration = (end_time - start_time).seconds
        
        # Display final answer
        print("\n" + "="*60)
        print("📊 FINAL ANSWER")
        print("="*60)
        print(results["final_answer"])
        print(f"\n⏱️  Completed in {duration} seconds by 3 agents")
        print("="*60)
        
        # Log conversation
        conversation_log.append({
            "timestamp": start_time.isoformat(),
            "question": user_input,
            "answer": results["final_answer"],
            "agents_used": list(results.keys())
        })
        
        # Save log
        with open("conversation_log.json", "w") as f:
            json.dump(conversation_log, f, indent=2)


if __name__ == "__main__":
    main()
