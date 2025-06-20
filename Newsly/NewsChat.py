import customtkinter as ctk
import threading
from genralscraper import get_data
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langchain_core.messages import HumanMessage,SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from hinditexttospeach import speak_summary_streaming , stop_playback
from langchain.tools import StructuredTool

# Memory intialize
checkpointer = InMemorySaver()
store = InMemoryStore()
# Optional: if you're using pyttsx3 or similar, make sure stop() works
def stop_sound():
    print("Voice stopped.")
    # Add your voice-stopping logic here, like engine.stop() if using pyttsx3
    stop_playback()

speak_thread = None  # Global thread reference

def run_chat_ui(headline):
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")

    class ChatApp(ctk.CTk):
        def __init__(self):
            super().__init__()
            self.title("AI News Assistant")
            self.geometry("600x600")

            self.chat_frame = ctk.CTkFrame(self)
            self.chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

            self.chat_history = ctk.CTkTextbox(self.chat_frame, wrap="word", font=("Helvetica", 14))
            self.chat_history.pack(padx=10, pady=10, fill="both", expand=True)
            self.chat_history.configure(state="disabled")

            self.bottom_frame = ctk.CTkFrame(self)
            self.bottom_frame.pack(fill="x", padx=10, pady=(0, 10))

            self.entry = ctk.CTkEntry(self.bottom_frame, width=350, height=40, font=("Helvetica", 14))
            self.entry.pack(side="left", padx=(0, 10), pady=10)
            self.entry.bind("<Return>", self.send_message)

            self.send_btn = ctk.CTkButton(self.bottom_frame, text="Send", command=self.send_message)
            self.send_btn.pack(side="left", padx=(0, 10))

            self.stop_btn = ctk.CTkButton(self.bottom_frame, text="Stop Sound", fg_color="red", command=stop_sound)
            self.stop_btn.pack(side="left")

        def send_message(self, event=None):
            user_input = self.entry.get().strip()
            if user_input:

                self.append_chat("You", user_input)
                self.entry.delete(0, "end")
                threading.Thread(target=self.handle_agent, args=(user_input,)).start()

        def handle_agent(self, ask):
            global speak_thread
            try:

                def execute(agent,msg):
                    response = agent.invoke({"messages":[HumanMessage(content=msg)]},{"configurable":{"thread_id":0}})
                    return (response["messages"][-1]).content

                tools = [get_data]

                instructions = """
                You are a reliable, professional news assistant.

Your job is to help users understand any news topic they ask about. You will receive a headline, keyword, or question. Based on that, retrieve accurate and complete information, and answer all follow-up questions using that data.
Use the Tool whenever Required and once at the starting of the conversation, and do not use the tool if you can answer the user without tool.
Before using tool properly format your  query according to the users the question.
---

🔍 INFORMATION ACCESS BEHAVIOR:

1. Retrieve full data at the beginning of the conversation.
2. If the user asks about:
   - A **specific fact** (like a country’s involvement, exact date, name, location) that you do **not already know**, or
   - Introduces a **new entity, angle, or context** not mentioned in the original result,  
   → **You must retrieve additional data** immediately and silently.
3. Do **not retrieve data multiple times unnecessarily**. Reuse existing knowledge when answering repeated or covered questions.
4. Never reveal or mention that you're retrieving or searching data. Keep all internal operations hidden from the user.

---

🧠 RESPONSE BEHAVIOR:

- If you know the answer, give it directly and clearly.
- If you do not know the answer and retrieval is allowed, silently fetch the necessary data and answer.
- If you cannot find a specific detail after trying, respond honestly: say the detail is not publicly available or not mentioned.

---

📋 ANSWER FORMAT:

- Respond clearly and factually in English.
- Use bullet points or structure when summarizing a full event (optional but recommended).

---

🗣️ TONE:

- Be formal, helpful, and factual.
- Do not use slang or technical jargon unless the user does.
- Never mention tools, APIs, or memory to the user.

---

🎯 OBJECTIVE:

Deliver accurate, respectful answers using reliable data, retrieving new information only when required — and never breaking character.

                """
                instructions2 = """
                You will receive a English summary. Your task is to translate it into simple, conversational Hindi, like how normal people speak in real life. Avoid using formal or pure Hindi words. Use simple and common Hindi vocabulary, and include basic English terms like "app", "video", "tool", "update", etc., if they feel natural.

                Only output the translated Hindi sentence.
                Do not use * or something else keep the output simple looking.
                """

                llm = ChatGoogleGenerativeAI(
                    model="gemini-2.0-flash",
                    api_key="Your_API",
                    temperature=0.5
                )

                agent = create_react_agent(
                    llm,
                    tools=tools,
                    prompt=SystemMessage(content=instructions),
                    store=store,
                    checkpointer=checkpointer

                )

                hindi = create_react_agent(
                    llm,
                    tools=[],
                    prompt=SystemMessage(content=instructions2)
                )
                execute(agent,headline)
                data = f"Instructions : {instructions},What user asked: {ask}"
                summary = execute(agent,data)

                self.append_chat("Agent", summary)

                translation = execute(hindi,f"Convert this into simplified Hinglish and write it in Hindi Text (only return Hindi text): {summary}")
                translation = str(translation).replace("*","")
                self.append_chat("Hindi", translation)

                # Run speak in a thread so it doesn't block UI
                speak_thread = threading.Thread(target=speak_summary_streaming, args=(translation,1.3))
                speak_thread.start()

            except Exception as e:
                self.append_chat("Agent", f"Error: {str(e)}")

        def append_chat(self, sender, message):
            self.chat_history.configure(state="normal")

            tag = "user_tag" if sender == "You" else "agent_tag"

            # Insert tagged sender name
            self.chat_history.insert("end", f"{sender}: ", tag)
            self.chat_history.insert("end", f"{message}\n\n")

            # Only color styling (no font allowed!)
            self.chat_history.tag_config("user_tag", foreground="#1e88e5")
            self.chat_history.tag_config("agent_tag", foreground="#43a047")

            self.chat_history.configure(state="disabled")
            self.chat_history.yview("end")

    app = ChatApp()
    app.mainloop()

if __name__ == "__main__":
    run_chat_ui("Iran Israel war live updates: Iran's Arak nuclear site hit, Israeli hospital struck as missile fire intensifies")
