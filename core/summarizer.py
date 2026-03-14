def summarize_conversation(llm, memory):
    conversation_text = ""
    for msg in memory.get():
        conversation_text += f"{msg['role']}: {msg['content']}\n"

    prompt = [
        {
            "role": "system",
            "content": "Summarize important facts, events, and user preferences from this conversation briefly."
        },
        {
            "role": "user",
            "content": conversation_text
        }
    ]

    summary = llm.generate(prompt)
    return summary