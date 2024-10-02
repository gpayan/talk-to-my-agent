import os
from typing import Any, List, Optional, Dict
import json

from dotenv import load_dotenv
from openai import OpenAI

from demarches_simplifiees import list_demarches_simplifiees, demarches_simplifiees_function_schemas

load_dotenv()

class DemarchesSimplifieesAgent:

    SYSTEM_MESSAGE_TEMPLATE_LEGACY = """
    Vous êtes l'agent de Démarches Simplifiées. Votre objectif est d'aider l'utilisateur avec sa demande.
    Vous ne parlez qu'en français.
    Votre but est de collecter les informations de l'utilisateur, spécifiquement son nom, son email et son numéro de téléphone.
    Vous pouvez demander à l'utilisateur son nom, son email et son numéro de téléphone.

    L'historique de votre conversation avec l'utilisateur est :
    {conversation_history}
    """

    SYSTEM_MESSAGE_TEMPLATE = """
    Vous êtes l'agent de Démarches Simplifiées. Votre objectif est d'aider l'utilisateur avec sa demarche de {demarche} qui vise a {description}.
    Vous ne parlez qu'en français.
    Votre but est de collecter les informations de l'utilisateur pour l'assister dans sa demarche, spécifiquement {required_data}.
    Vous pouvez demander à l'utilisateur les informations requises pour cette demarche.

    Vous avez deja collecte les informations suivantes: {collected_data}.
    Il vous manque les informations suivantes: {missing_data}.

    L'historique de votre conversation avec l'utilisateur est :
    {conversation_history}
    """

    SYSTEM_MESSAGE_IDENTIFICATION_DEMARCHES_TEMPLATE = """
    Vous êtes l'agent de Démarches Simplifiées. Votre objectif est d'aider l'utilisateur avec sa demande.
    Vous ne parlez qu'en français.
    Vous allez recevoir une demande utilisateur et vous devez identifier la démarche associée.
    Vous retournez un objet JSON, avec le format suivant:
        'demarche': <le nom de la démarche parmi la liste des démarches simplifiées ci-dessous: demande_acte_etat_civil,declaration_changement_coordonnees, operation_tranquilite_vacances, correction_erreur_etat_civil, situation_electorale, rendez_vous_gendarmerie, rendez_vous_commissariat, vehicule_en_fourriere>,
        ET
        'required_data': <la liste des données requises pour cette démarche>

    Si aucune démarche n'est identifiée, retournez une liste vide.

    La liste des démarches simplifiées est la suivante:
    {list_demarches_simplifiees}
    """

    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.conversation_history: List[dict] = []
        self.demarche = None
        self.description = None
        self.required_data_dict = None

    def update_system_message(self) -> str:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        collected_data = json.dumps({key: value for key, value in self.required_data_dict.items() if value})
        missing_data = json.dumps({key: value for key, value in self.required_data_dict.items() if not value})

        return self.SYSTEM_MESSAGE_TEMPLATE.format(
            conversation_history=history_str,
            demarche=self.demarche,
            description=self.description,
            required_data=json.dumps(list(self.required_data_dict.keys())),
            collected_data=collected_data,
            missing_data=missing_data,
        )
    
    def update_system_message_with_demarche(self) -> str:
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in self.conversation_history])
        collected_data = json.dumps({key: value for key, value in self.required_data_dict.items() if value})
        missing_data = json.dumps({key: value for key, value in self.required_data_dict.items() if not value})

        return self.SYSTEM_MESSAGE_TEMPLATE.format(
            conversation_history=history_str,
            demarche=self.demarche,
            description=self.description,
            required_data=json.dumps(list(self.required_data_dict.keys())),
            collected_data=collected_data,
            missing_data=missing_data
        )

    def identify_demarches(self, message_to_analyze: str) -> Dict[str, Any]:
        messages = [
            {'role': 'system', 'content': self.SYSTEM_MESSAGE_IDENTIFICATION_DEMARCHES_TEMPLATE.format(
                list_demarches_simplifiees=self._format_list(list_demarches_simplifiees)
            )},
            {'role': 'user', 'content': message_to_analyze}
        ]

        try:
            response = self.openai_client.chat.completions.create(
                model = "gpt-4o",
                messages = messages,
                temperature = 0,
                response_format = {"type": "json_object"}
            )
            answer = response.choices[0].message.content

            answer_json = json.loads(answer)
            self.demarche = answer_json.get('demarche')
            self.description = answer_json.get('description')

            list_required_data = answer_json.get('required_data')
            dict_required_data = { data_field : None for data_field in list_required_data}
            self.required_data_dict = dict_required_data

            return answer
        except Exception as e:
            raise Exception(f"Error while getting answer from OpenAI: {e}")

    def get_answer(self, question: str) -> str:

        self.conversation_history.append({"role": "user", "content": question})

        '''
        messages = [
            {'role': 'system', 'content': self.update_system_message()},
            *self.conversation_history
        ]
        '''
        
        messages = [
            {'role': 'system', 'content': self.update_system_message_with_demarche()},
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
    def _format_list(data: List[Dict[str, Any]]) -> str:
        return "\n\n".join(["\n".join([f"{key}: {value}" for key, value in data_element.items()]) for data_element in data])

    def update_user_data(self, response):
        for key in response.keys():
            if response.get(key):
                self.required_data_dict[key] = response[key]

    def get_required_data(self):
        return all(value for value in self.required_data_dict.values())

    def validate_required_data(self, message: str) -> bool:

        missing_data = [key for key, value in self.required_data_dict.items() if not value]
        #print('Missing data:', missing_data)

        system_message = f"""
        Vous êtes l'agent de Démarches Simplifiées. Votre objectif est d'aider l'utilisateur avec sa demarche de {self.demarche} qui vise a {self.description}.
        Votre tache est d'extraire les informations requises pour cette demarche du message partage par l'utilisateur.
        Les informations que vous cherchez a extraire sont: {json.dumps(missing_data)}
        Tu ne retournera qu'un seul objet JSON, avec les informations extraites.
        Si aucune information n'est extraite, retourne un objet JSON vide.
        """

        response = self.openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': message}
            ],
            response_format = {"type": "json_object"}
        )

        answer = response.choices[0].message.content
        answer_json = json.loads(answer)

        # Update user data
        for key, value in answer_json.items():
            if value:
                self.required_data_dict[key] = value
                print(f'Updated field {key} with value {value}')
        
        missing_data = [key for key, value in self.required_data_dict.items() if not value]
        print('Missing data:', missing_data)
        
        # missing_data = [key for key, value in self.required_data_dict.items() if not value]
        # print('Missing data:', missing_data)
        return self.get_required_data()

        '''    
        resp = self.openai_client.chat.completions.create(
            model = "gpt-4o",
            messages = [
                {'role': 'system', 'content': system_message},
                {'role': 'user', 'content': message}
            ],
            tools = demarches_simplifiees_function_schemas,
            tool_choice = "required"
        )

        response = resp.choices[0].message
        print(response)
        tool_calls = response.tool_calls

        if tool_calls:
            function_name = tool_calls[0].function.name
            print('Function name:', function_name)
            function_args = json.loads(tool_calls[0].function.arguments)
            print('Function args:', function_args)

            # Update user data
            for key, value in function_args.items():
                if value:
                    self.required_data_dict[key] = value
                    print(f'Updated field {key} with value {value}')

            print('Do we have all the data that we need?', self.get_required_data())
            missing_data = [key for key, value in self.required_data_dict.items() if not value]
            print('Missing data:', missing_data)
            return missing_data
        '''
