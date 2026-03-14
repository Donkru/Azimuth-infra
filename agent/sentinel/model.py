from config import SYSTEM_PROMPT


class LocalModel:
    def __init__(self) -> None:
        self.system_prompt = SYSTEM_PROMPT

    def generate(self, user_message: str, history: list[dict]) -> str:
        history_text = " | ".join(f"{m['role']}: {m['content']}" for m in history[-4:])
        return (
            f"[local-dev-reply]\n"
            f"system={self.system_prompt}\n"
            f"history={history_text}\n"
            f"user={user_message}\n\n"
            f"This is a placeholder response from your server-side chatbot."
        )
