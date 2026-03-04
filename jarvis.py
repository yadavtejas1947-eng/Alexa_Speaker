from __future__ import annotations

import os
import shlex
import subprocess
import threading
import time
from dataclasses import dataclass
from datetime import datetime

from openai import OpenAI


SYSTEM_PROMPT = (
    "You are JARVIS, a concise, helpful AI assistant. "
    "Provide practical, actionable responses."
)


@dataclass
class Reminder:
    seconds: int
    message: str


class JarvisAssistant:
    def __init__(self) -> None:
        self.client = None
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            self.client = OpenAI(api_key=api_key)

    def run(self) -> None:
        print("JARVIS online. Type 'help' for commands, 'exit' to quit.")
        while True:
            try:
                user_input = input("you> ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\nJARVIS offline.")
                break

            if not user_input:
                continue

            if user_input.lower() in {"exit", "quit"}:
                print("JARVIS offline.")
                break

            response = self.handle_input(user_input)
            if response:
                print(f"jarvis> {response}")

    def handle_input(self, user_input: str) -> str:
        tokens = user_input.split()
        command = tokens[0].lower()

        if command == "help":
            return (
                "Commands: time | remind <seconds> <message> | "
                "run <shell command> | help | exit"
            )

        if command == "time":
            return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if command == "remind":
            return self._set_reminder(tokens)

        if command == "run":
            return self._run_shell(user_input)

        return self._ask_llm(user_input)

    def _set_reminder(self, tokens: list[str]) -> str:
        if len(tokens) < 3:
            return "Usage: remind <seconds> <message>"

        try:
            seconds = int(tokens[1])
        except ValueError:
            return "Seconds must be an integer."

        message = " ".join(tokens[2:])
        reminder = Reminder(seconds=seconds, message=message)

        thread = threading.Thread(target=self._reminder_worker, args=(reminder,), daemon=True)
        thread.start()
        return f"Reminder set for {seconds}s: {message}"

    def _reminder_worker(self, reminder: Reminder) -> None:
        time.sleep(reminder.seconds)
        print(f"\njarvis> ⏰ Reminder: {reminder.message}")

    def _run_shell(self, user_input: str) -> str:
        shell_cmd = user_input[len("run") :].strip()
        if not shell_cmd:
            return "Usage: run <shell command>"

        parts = shlex.split(shell_cmd)
        if not parts:
            return "No shell command provided."

        forbidden = {"sudo", "rm", "reboot", "shutdown"}
        if parts[0] in forbidden:
            return f"Blocked command: {parts[0]}"

        try:
            completed = subprocess.run(
                parts,
                capture_output=True,
                text=True,
                timeout=10,
                check=False,
            )
        except Exception as exc:  # noqa: BLE001
            return f"Shell error: {exc}"

        output = completed.stdout.strip() or completed.stderr.strip() or "(no output)"
        return f"[{completed.returncode}] {output}"

    def _ask_llm(self, user_input: str) -> str:
        if not self.client:
            return (
                "I can answer built-in commands right now. "
                "Set OPENAI_API_KEY to enable general AI chat."
            )

        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": user_input},
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content or "(empty response)"
        except Exception as exc:  # noqa: BLE001
            return f"LLM request failed: {exc}"


if __name__ == "__main__":
    JarvisAssistant().run()
