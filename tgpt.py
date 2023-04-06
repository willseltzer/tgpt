#!/usr/bin/env python3
import os
from typing import List, Mapping, Optional
from prompts import (
    REWRITE_CODE_PROMPT,
    VERIFY_CODE_PROMPT,
)

if REWRITE_CODE_PROMPT or not VERIFY_CODE_PROMPT:
    raise ValueError(
        "Please populate REWRITE_CODE_PROMPT, and VERIFY_CODE_PROMPT before running in prompts.py"
    )
import openai
from halo import Halo
from prompt_toolkit import print_formatted_text
from prompt_toolkit.formatted_text import FormattedText
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.styles import Style
from prompt_toolkit import PromptSession
from system_prompt import helpful_assistant
from system_prompt import SystemPrompt


class GPT:
    def __init__(
        self,
        system_prompt: SystemPrompt,
        model: str = "gpt-3.5-turbo",
        output_print_style: Style = Style.from_dict(
            {
                "assistant_prefix": "bold #2AD2C9",
                "assistant_input": "#00E5FF",
            }
        ),
        messages: Optional[List[Mapping[str, str]]] = [],
    ) -> None:
        self.messages = []
        self.system_prompt = system_prompt
        self.messages.append({"content": system_prompt.prompt, "role": "system"})
        self.messages.extend(messages)
        self.model = model
        self.output_print_style = output_print_style
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def _add_user_message(self, message: str) -> None:
        self.messages.append({"content": message, "role": "user"})

    def _add_assistant_message(self, message) -> None:
        if "role" not in message or "content" not in message:
            return
        self.messages.append({"content": message["content"], "role": message["role"]})

    def __call__(self, prompt: str, stream=True) -> str:
        self._add_user_message(prompt)
        try:
            spinner_text = (
                "Getting ready to stream..."
                if stream
                else "Responding in batch. More of a waterfall and less of a stream."
            )
            spinner = Halo(text=spinner_text, spinner="dots")
            spinner.start()
            response = openai.ChatCompletion.create(
                model=self.model, messages=self.messages, stream=stream
            )
            if not stream:
                self._add_assistant_message(response)
                spinner.stop()
                return response["choices"][0]["message"]["content"]
            else:
                spinner.stop()
                return response
        except openai.error.RateLimitError as e:
            print("\n\033[91m\033[1mYou've hit the openai rate limit.\033[0m")
            print("\033[91mError details:\033[0m", e)

    def stream(self, prompt: str) -> str:
        response = self.__call__(prompt, stream=True)
        collected_events = []
        complete_assistant_response = ""
        # iterate through the stream of events
        for event in response:
            collected_events.append(event)  # save the event response
            chunk_message = event["choices"][0]["delta"]
            complete_assistant_response += chunk_message.get("content", "")
            yield (chunk_message.get("content", ""))
        self._add_assistant_message(
            {"role": "assistant", "content": complete_assistant_response}
        )

    def format_and_print_assistant_prefix(self) -> None:
        formatted_text = FormattedText(
            [
                (
                    "class:assistant_prefix",
                    f"\nAssistant({self.model}, system_prompt={self.system_prompt.name}):\n",
                ),
            ]
        )
        print_formatted_text(formatted_text, style=self.output_print_style, end="")

    def format_and_print_llm_response(
        self, response: str, indent=False
    ) -> FormattedText:
        response = f"    {response}" if indent else response
        formatted_text = FormattedText(
            [
                ("class:assistant_input", f"{response}"),
            ]
        )
        print_formatted_text(formatted_text, style=self.output_print_style, end="")


def batch_ask(msg: str) -> str:
    try:
        response = llm(msg, stream=False)
        return response
    except openai.error.RateLimitError as e:
        print("\n\033[91m\033[1mYou've hit the openai rate limit.\033[0m")
        print("\033[91mError details:\033[0m", e)


def remove_code_block(text: str) -> str:
    text = text.replace("```python", "")
    text = text.replace("```", "")
    return text


def code_from_file(file_path: str) -> str:
    code_file_to_rewrite = os.path.abspath(file_path)
    with open(code_file_to_rewrite, "r") as f:
        code = f.read()
    return code


if __name__ == "__main__":
    llm = GPT(
        system_prompt=help,
        model="gpt-4",
    )

    bindings = KeyBindings()

    @bindings.add("c-m")  # Ctrl+Enter
    def _(event):
        event.current_buffer.validate_and_handle()

    session = PromptSession()
    while True:
        user_input = session.prompt(
            FormattedText([("class:user_prefix", "User: ")]),
            style=Style.from_dict(
                {"user_prefix": "bold #FF4081", "user_input": "#49C0FF"}
            ),
            wrap_lines=True,
            multiline=True,
            key_bindings=bindings,
            complete_style="class:user_input",
        )

        if user_input.lower() == "exit":
            break
        elif user_input.lower().startswith(".verify"):
            if len(user_input.split()) == 2:
                code_file_to_verify = user_input.split()[1]
                code_to_verify = code_from_file(code_file_to_verify)
                msg_to_llm = VERIFY_CODE_PROMPT + code_to_verify
                response = batch_ask(msg_to_llm)
                llm.format_and_print_assistant_prefix()
                llm.format_and_print_llm_response(response)
            else:
                print("You need to provide a word to verify")
                continue
        elif user_input.lower().startswith(".rewrite"):
            # check for a word after rewrite
            if len(user_input.split()) == 2:
                code_file_to_rewrite = user_input.split()[1]
                code_to_rewrite = code_from_file(code_file_to_rewrite)
                msg_to_llm = REWRITE_CODE_PROMPT + code_to_rewrite
                response = batch_ask(msg_to_llm)
                response = remove_code_block(response)
                draft_filename = f"{code_file_to_rewrite}.draft"
                # now write the code
                with open(draft_filename, "w") as f:
                    f.write(response)
                llm.format_and_print_assistant_prefix()
                llm.format_and_print_llm_response(
                    f"I've rewritten the code for you to the file {draft_filename}\n"
                )
            else:
                print("You need to provide a word to rewrite")
                continue
        else:
            msg_to_llm = user_input
            llm.format_and_print_assistant_prefix()
            for idx, token in enumerate(llm.stream(msg_to_llm)):
                if idx == 0:
                    llm.format_and_print_llm_response(token, indent=True)
                else:
                    llm.format_and_print_llm_response(token)
            print("\n")
