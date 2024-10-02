import os
from typing import Any, List, Optional, Dict

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

class MyAgent:

    SYSTEM_MESSAGE_TEMPLATE = """
    Vous êtes la personne décrite ci-dessous:
    {my_data}

    Vous dialoguez avec l'agent virtuel de Démarches Simplifiées.
    Votre objectif est de {objective}.

    L'historique de votre conversation avec l'agent est :
    {conversation_history}
    """

    INIATE_DISCUSSION_MESSAGE = """
    Vous êtes la personne décrite ci-dessous:
    {my_data}

    Vous dialoguez avec l'agent virtual de Démarches Simplifiées.
    Votre objectif est de {objective}.

    Vous initiez la conversation en detaillant la demande que vous avez.
    """

    def __init__(self, my_data: Optional[Dict[str, Any]] = None,
                 objective: Optional[str] = None):
        self.my_data = my_data or {}
        self.conversation_history: List[Dict[str, str]] = []
        self.objective = objective
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    def initiate_discussion(self) -> str:

        messages = [
            {'role': 'system', 'content': self.INIATE_DISCUSSION_MESSAGE.format(
                my_data=self._format_dict(self.my_data),
                objective=self.objective
            )},
        ]

        try:
            response = self.openai_client.chat.completions.create(
                model = "gpt-4o",
                messages = messages,
                temperature = 0,
            )
            answer = response.choices[0].message.content
            self.conversation_history.append({"role": "user", "content": answer})
            return answer
        except Exception as e:
            raise Exception(f"Error while getting initial discussion message from OpenAI: {e}")

    def get_my_data(self) -> Dict[str, Any]:
        return self.my_data

    def set_my_data(self, my_data: Dict[str, Any]) -> bool:
        self.my_data = my_data
        return True

    def update_user_data(self, my_updated_data: Any) -> None:
        return

    def update_system_message(self) -> str:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        return self.SYSTEM_MESSAGE_TEMPLATE.format(
            my_data=self._format_dict(self.my_data),
            objective=self.objective,
            conversation_history=history_str
        )

    def get_answer(self, agent_response: str) -> str:

        # the agent_response is our user message
        self.conversation_history.append({"role": "user", "content": agent_response})

        messages = [
            {'role': 'system', 'content': self.update_system_message()},
            *self.conversation_history
        ]

        try:
            response = self.openai_client.chat.completions.create(
                model = "gpt-4o",
                messages = messages,
                temperature = 0,
            )
            answer = response.choices[0].message.content

            self.conversation_history.append({"role": "assistant", "content": answer})
            return answer
        except Exception as e:
            raise Exception(f"Error while getting answer from OpenAI: {e}")

    @staticmethod
    def _format_dict(data: Dict[str, Any]) -> str:
        return "\n".join([f"{key}: {value}" for key, value in data.items()])

    def reset_conversation(self) -> None:
        self.conversation_history = []