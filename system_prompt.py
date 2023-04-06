from dataclasses import dataclass


@dataclass
class SystemPrompt:
    name: str
    prompt: str


code_min_token = SystemPrompt(
    "helpful_assistant",
    """You're a helpful assistant. You answer questions helpfully and succinctly.""",
)
