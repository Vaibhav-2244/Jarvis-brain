from core.llm import LLM
from core.memory import ConversationMemory
from core.state import ConversationState
from core.prompt import build_messages
from core.retriever import retrieve_context
from core.user_manager import UserManager
from core.summarizer import summarize_conversation
from core.face_recognition import FaceRecognizer
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def main():

    jarvis = LLM(GROQ_API_KEY)
    memory = ConversationMemory(max_turns=6)
    state = ConversationState()
    knowledge = retrieve_context()
    users = UserManager()

    print("\nJARVIS Booting...\n")

    # -------- FACE RECOGNITION --------
    face_system = FaceRecognizer()

    print("Looking for known user...")

    username = face_system.recognize()

    # -------- UNKNOWN USER --------
    if username == "unknown":

        username = None

        print(
            "\nJARVIS: Hello there. "
            "If you'd like me to remember you, just say 'register me'.\n"
        )

    # -------- KNOWN USER --------
    else:

        print(f"\nFace recognized: {username}\n")

        profile, existed = users.load_user(username)

        if existed:
            print(f"JARVIS: Welcome back, {profile['name']}.\n")
        else:
            print(f"JARVIS: Hello {profile['name']}, nice to meet you.\n")

    # -------- MAIN LOOP --------
    while True:

        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("JARVIS: Shutting down.")
            break

        command = user_input.lower()

        # -------- REGISTER FACE COMMAND --------
        if "register me" in command:

            print("JARVIS: Sure. What should I call you?")
            name = input("Enter name: ").strip()

            print("JARVIS: Please look at the camera. Registering you now...")

            success = face_system.register_new_user(name)

            if success:

                username = name

                profile, existed = users.load_user(username)

                print(f"JARVIS: Nice to meet you {name}. I will remember you.\n")

            else:
                print("JARVIS: Sorry, I cannot register more users right now.")

            continue

        # -------- UPDATE STATE --------
        state.update_from_text(user_input)

        messages = build_messages(
            user_input,
            memory,
            state,
            knowledge
        )

        # Inject user context only if registered
        if username:
            user_context = users.get_context_block()
            messages.insert(1, {"role": "system", "content": user_context})

        response = jarvis.generate(messages)

        print(f"\nJARVIS: {response}\n")

        memory.add("user", user_input)
        memory.add("assistant", response)

        # After 8 turns → summarize + store
        if len(memory.get()) >= 8 and username:

            summary = summarize_conversation(jarvis, memory)

            users.add_summary(summary)

            memory.history.clear()


if __name__ == "__main__":
    main()