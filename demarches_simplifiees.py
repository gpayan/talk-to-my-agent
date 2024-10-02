list_demarches_simplifiees = [
    {
        "demarche": "demande_acte_etat_civil",
        "description": "Demander auprès des communes un acte de naissance, mariage ou décès",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe",
            "filiation",
            "situation familiale",
            "adresse"
        ]
    },
    {
        "demarche": "declaration_changement_coordonnees",
        "description": "Informer plusieurs organismes d'un changement d'adresse passé ou à venir",
        "required_data": [
            "nom",
            "prenom",
            "sexe",
            "numero fiscal",
            "numero de securite sociale",
            "adresse actuelle",
            "adresse future"
        ]
    },
    {
        "demarche": "operation_tranquilite_vacances",
        "description": "Permet aux particuliers signaler à la Police et la gendarmenie une absensce prolongé de leur dominicile principale (et secondaire sur les zones gendarmerie)",
        "required_data": [
            "nom",
            "prenom",
            "adresse",
            "adresse logement vacant",
            "date de depart",
            "date de retour",
            "dispositif de protection du domicile",
            "personne de confiance",
            "informations d'acces a la residence",
        ]
    },
    {
        "demarche": "correction_erreur_etat_civil",
        "description": "En cas d'erreur sur les informations personnelles remontées sur la carte électorale, FranceConnect ou la carte vitale.",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe",
            "erreur a corriger",
        ],
    },
    {
        "demarche": "situation_electorale",
        "description": "Vérifier son inscription sur les listes électorales et son bureau de vote.",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe"
        ],
    },
    {
        "demarche": "rendez_vous_gendarmerie",
        "description": "Prendre rendez-vous en gendarmerie",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe"
        ],
    },
    {
        "demarche": "rendez_vous_commissariat",
        "description": "Prendre rendez-vous en commissariat",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe"
        ],
    },
    {
        "demarche": "vehicule_en_fourriere",
        "description": "Retrouver un vehicule mis en fourriere",
        "required_data": [
            "nom",
            "prenom",
            "date de naissance",
            "lieu de naissance",
            "sexe",
            "plaque d'immatriculation du vehicule",
        ]
    }
]


demarches_simplifiees_function_schemas = [
    {
        "type": "function",
        "function": {
            "name": "situation_electorale",
            "description": "Vérifier son inscription sur les listes électorales et son bureau de vote.",
        },
        "parameters": {
            "type": "object",
            "properties": {
                "nom": {
                    "type": "string",
                    "description": "Nom de la personne concernée"
                },
                "prenom": {
                    "type": "string",
                    "description": "Prenom de la personne concernée"
                },
                "date de naissance": {
                    "type": "string",
                    "description": "Date de naissance de la personne concernée"
                },
                "lieu de naissance": {
                    "type": "string",
                    "description": "Lieu de naissance de la personne concernée"
                },
                "sexe": {
                    "type": "string",
                    "description": "Sexe de la personne concernée"
                }
            },
            "required": []
        }
    },
]