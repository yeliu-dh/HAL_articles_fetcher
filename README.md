# HAL Fetcher API

**HAL Articles Fetcher** est une application web interactive construite avec **Streamlit** qui permet de rechercher et d’extraire des articles depuis la plateforme [HAL](https://hal.science/) via API.

Elle permets de chercher flexiblement des articles par année et par mois et garde la plupart des des filtrage d'HAL (Type de documents, domaines, mots-clés, langues, labs...).

Le fichier de résultat est en **CSV** avec les colonnes choisies  

**Cliquez ici** [APP](https://hal-articles-fetcher.streamlit.app/) pour commencer directement!🚀


## 📂 Structure du projet

HAL-fetcher_api/
│
├── src/
│ ├── app.py               # Entrée principale Streamlit
│ ├── HAL_search_api.py    # Fonctions pour interroger l’API HAL
│ └── facets/              # Informations pour les menus
│ ├── doctype_map.py
│ ├── domaine_map.py
│ └── lang_map.py
│
├── .gitignore
├── README.md
└── requirements.txt # Dépendances Python

