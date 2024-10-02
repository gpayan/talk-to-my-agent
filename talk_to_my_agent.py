import json

from my_agent import MyAgent
from demarches_simplifiees_agent import DemarchesSimplifieesAgent

if __name__ == '__main__':

    with open("my_data_cookie.txt", "r", encoding="utf-8") as file:
        MY_DATA = json.load(file)

    delimiter = '-----'
    print(f'\n{delimiter}ETAPE 1: Usager pose une question a son IA{delimiter}\n')

    user_objective = input("Bonjour, que puis-je faire pour vous ?\n")
    
    my_agent = MyAgent(my_data = MY_DATA,
                       objective=user_objective)

    agent_demarches_simplifiees = DemarchesSimplifieesAgent()

    my_agent_message = my_agent.initiate_discussion()
    print(f"\n{delimiter}ETAPE 2: Mon IA pose une question a l'IA de Demarches Simplifiees{delimiter}\n")
    print(my_agent_message)
    input()

    '''
    test_messages = [
        "Je veux aller voir la gendarmerie",
        "Je vais partir en vacances et laisser ma maison vide",
        "Je demenage et je dois changer mon adresse",
        "Je besoin d'un acte de naissance",
        "Je veux savoir si je suis inscrit sur les listes electorales",
    ]

    for msg in test_messages:
        print(msg)
        agent_demarches_simplifiees_message = agent_demarches_simplifiees.identify_demarches(msg)
        print('Agent Demarches Simplifiees:')
        print(f'{agent_demarches_simplifiees_message}')
        input()
    '''
    print(f"\n{delimiter}ETAPE 3: Demarches Simplifiees cherche a identifier la bone demarche{delimiter}\n")
    identification_demarche = agent_demarches_simplifiees.identify_demarches(my_agent_message)
    if identification_demarche:
        print('Demarche identifiee:', identification_demarche)
        
        print(f"\n{delimiter}ETAPE 4: L'IA de Demarches Simplifiees regarde si elle dispose de toutes les donnees dont elle a besoin.{delimiter}\n")
        all_data_collected = agent_demarches_simplifiees.validate_required_data(my_agent_message)

        print('Est-ce que Demarches Simplifiees a toutes les donnees necessaire pour la demarche ?', all_data_collected)

        while all_data_collected is False:

            print(f"\n{delimiter}ETAPE Suivante: Demarches Simplifiees demande a l'IA de l'usager les donnees manquantes{delimiter}\n")

            agent_demarches_simplifiees_message = agent_demarches_simplifiees.get_answer(my_agent_message)
            print('Agent Demarches Simplifiees:')
            print(f'{agent_demarches_simplifiees_message}')
            input()

            # print(f"\n{delimiter}ETAPE Suivante: L'IA Demarches Simplifiees verifie quelles nouvelles donnees sont entrees{delimiter}\n")
            all_data_collected = agent_demarches_simplifiees.validate_required_data(my_agent_message)
            print('Avons-nous toutes les donnes dont nous avons besoin ?', all_data_collected)
            input()

            print(f"\n{delimiter}ETAPE Suivante: Mon IA recupere et envoie les donnees manquantes a Demarches Simplifiees{delimiter}\n")
            my_agent_message = my_agent.get_answer(agent_demarches_simplifiees_message)
            print('Mon Agent:')
            print(f'{my_agent_message}')
            input()

        print('Toutes les donnees ont ete collectees')
        print(f"\n{delimiter}ETAPE Presque-Finale: Toutes les donnees necessaire a la demarche ont ete collectees.{delimiter}\n")

        print(f"\n{delimiter}ETAPE Finale: Execution de la demarche!{delimiter}\n")
        print('Demarche:', agent_demarches_simplifiees.demarche)
        print('Donnees:', agent_demarches_simplifiees.required_data_dict)
        '''    
        for i in range(5):
            agent_demarches_simplifiees_message = agent_demarches_simplifiees.get_answer(my_agent_message)
            print('Agent Demarches Simplifiees:')
            print(f'{agent_demarches_simplifiees_message}')
            input()
            my_agent_message = my_agent.get_answer(agent_demarches_simplifiees_message)
            print('Mon Agent:')
            print(f'{my_agent_message}')
            input()
        '''