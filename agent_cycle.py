"""Autonomous agent cycle with integrated memory retrieval."""

from openai import OpenAI
from memory_layer import SharedMemoryLayer


class AutonomousBot:
    """Main bot class with memory-enabled turn processing."""
    
    def __init__(self):
        self.llm = OpenAI()
        self.memory_module = SharedMemoryLayer()

    def process_turn(self, user_id: str, user_input: str) -> str:
        """
        Process a single turn through the agent cycle with memory enrichment.
        
        Steps:
        1. Retrieve relevant past facts from memory
        2. Construct enriched system prompt
        3. Execute main LLM cycle
        4. Save new context asynchronously (background)
        """
        # Step 1: Context preparation subagent
        print("[Log] Retrieving relevant memories...")
        past_facts = self.memory_module.fetch_relevant_facts(user_input, user_id=user_id)

        # Step 2: System prompt construction
        system_prompt = f"""Ты — интеллектуальный агент-помощник.
Опирайся на следующие известные факты о пользователе для персонализации ответа:
{past_facts}

Если фактов нет, просто отвечай на запрос пользователя."""

        # Step 3: Main execution cycle
        response = self.llm.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input}
            ]
        )
        agent_reply = response.choices[0].message.content

        # Step 4: Asynchronous/background memory update
        # (In production, move this to a separate thread or queue)
        print("[Log] Saving new facts to Mem0...")
        self.memory_module.store_cycle_context(user_input, agent_reply, user_id=user_id)

        return agent_reply


if __name__ == "__main__":
    bot = AutonomousBot()
    user = "alex_dev_01"

    print("--- Iteration 1 ---")
    query_1 = "Привет! Запомни, что я предпочитаю писать скрипты оптимизации систем на PowerShell, а для изоляции использую Docker."
    print("User:", query_1)
    print("Bot:", bot.process_turn(user_id=user, user_input=query_1))

    print("\n--- Iteration 2 (Memory Verification) ---")
    query_2 = "Как мне лучше автоматизировать глубокую очистку временных файлов в ОС Windows перед созданием образа?"
    print("User:", query_2)
    # Bot should recall PowerShell and Docker preferences via Mem0
    print("Bot:", bot.process_turn(user_id=user, user_input=query_2))

    print("\n[Debug] All stored facts in database:")
    for fact in bot.memory_module.debug_memory(user_id=user):
        print(f"- {fact['memory']}")