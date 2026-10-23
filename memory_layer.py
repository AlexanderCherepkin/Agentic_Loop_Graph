"""Memory management layer using Mem0 for agent context persistence."""

import os
from dotenv import load_dotenv
from mem0 import Memory


load_dotenv()


class SharedMemoryLayer:
    """
    Isolated memory layer accessible by subagents to enrich system prompts
    with current user facts.
    """
    
    def __init__(self):
        # Configure local storage in ChromaDB
        # Suitable for WSL or Docker container deployment
        config = {
            "vector_store": {
                "provider": "chroma",
                "config": {
                    "collection_name": "agent_memory_db",
                    "path": "./memory_storage"  # Persist data to disk
                }
            },
            "llm": {
                "provider": "openai",
                "config": {
                    "model": "gpt-4o-mini"
                }
            }
        }
        self.memory = Memory.from_config(config)

    def store_cycle_context(self, user_message: str, agent_response: str, user_id: str):
        """
        Background subagent for context saving.
        Mem0 automatically analyzes this array and saves only relevant facts.
        """
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": agent_response}
        ]
        self.memory.add(messages, user_id=user_id)

    def fetch_relevant_facts(self, current_task_query: str, user_id: str) -> str:
        """
        Method for the main cycle: retrieves facts semantically similar to the current query.
        """
        results = self.memory.search(query=current_task_query, user_id=user_id)

        if not results:
            return "Нет сохраненных фактов."

        # Results returns a list of dictionaries; convert to readable string format
        facts = [res["memory"] for res in results]
        return "\n".join(f"- {fact}" for fact in facts)

    def debug_memory(self, user_id: str):
        """Helper method to inspect all memory entries for a specific user."""
        return self.memory.get_all(user_id=user_id)


if __name__ == "__main__":
    # Quick test of the memory layer
    print("[Test] Initializing SharedMemoryLayer...")
    mem = SharedMemoryLayer()

    # Store some context
    user_message = "Привет! Я разработчик, предпочитаю Python и Docker."
    agent_response = "Здравствуйте! Чем я могу помочь вам в разработке?"
    
    print(f"[Test] Storing: {user_message}")
    mem.store_cycle_context(user_message, agent_response, user_id="test_user_01")

    # Fetch facts for a related query
    query = "Как оптимизировать производительность моего проекта?"
    facts = mem.fetch_relevant_facts(query, user_id="test_user_01")
    
    print(f"[Test] Query: {query}")
    print(f"Facts retrieved:\n{facts}")

    # Debug all memory for this user
    all_memory = mem.debug_memory(user_id="test_user_01")
    print(f"\n[Debug] All stored memories:")
    for item in all_memory:
        print(f"  - {item['memory']} (score: {item['match_score']:.2f})")