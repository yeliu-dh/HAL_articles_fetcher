# HAL Fetcher API

**HAL Articles Fetcher** est une application web interactive construite avec **Streamlit** qui permet de rechercher et d’extraire des articles depuis la plateforme [HAL](https://hal.science/) via API.

Elle permets de chercher flexiblement des articles par année et par mois et garde la plupart des filtrage sur HAL (Type de documents, domaines, mots-clés, langues, labs...).

Le fichier de résultat est en **CSV** avec les colonnes choisies  

**Cliquez ici** [APP](https://hal-articles-fetcher.streamlit.app/) pour commencer directement!🚀




## 📂 Structure du projet
```
HAL-fetcher_api/
│
├── src/
│   ├── app.py
│   ├── HAL_search_api.py
│   └── facets/
│       ├── doctype_map.py
│       ├── domaine_map.py
│       └── lang_map.py
├── .gitignore
├── README.md
└── requirements.txt
```

