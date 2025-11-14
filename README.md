# Agentic RAG MVP

Un projet de référence minimal pour la génération augmentée par récupération (RAG) qui démontre comment :

- Convertir des fiches produit PDF en JSON structuré avec [Docling](https://github.com/docling-project/docling).
- Générer des embeddings riches du contenu et des métadonnées via Google Generative AI.
- Stocker et interroger les vecteurs localement avec [Chroma](https://www.trychroma.com/).
- Orchestrer des conversations augmentées par récupération avec des agents LangChain propulsés par des modèles Cerebras.

Le code est volontairement compact afin que vous puissiez expérimenter l’ingestion de vos propres documents produits, affiner les filtres de métadonnées et explorer le comportement d’appels d’outils itératifs.

---

## 1. Prérequis

| Exigence | Remarques |
| --- | --- |
| Python ≥ 3.13 | `uv` est utilisé pour gérer l’environnement et les dépendances. |
| Clés API | `GOOGLE_API_KEY` pour les embeddings, `CEREBRAS_API_KEY` pour le LLM de chat. |
| Outils optionnels | Fiches PDF à ingérer (placées dans `documents/`). |

> **Astuce :** Copiez `.env.example` vers `.env` et renseignez les secrets requis avant d’exécuter les commandes.

---

## 2. Structure du projet

```
.
├── main.py                # Point d’entrée CLI pour indexer les documents et lancer l’agent de chat
├── ingest.py              # Pipeline d’ingestion PDF → JSON via Docling
├── rag_mvp/
│   ├── index_json.py      # Construction & persistance de l’index Chroma à partir des JSON traités
│   ├── tools.py           # Helpers de récupération et formatage des métadonnées
│   └── agent.py           # Agent LangChain avec comportement de récupération itératif
├── data/
│   ├── processed/         # Documents JSON générés par l’ingestion
│   └── index/chroma/      # Stockage de vecteurs Chroma persistant
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 3. Installation & préparation de l’environnement

1. **Cloner et entrer dans le projet**
   ```bash
   git clone <repo-url>
   cd rag-challenge
   ```

2. **Créer & activer un environnement virtuel** (via `uv`)
   ```bash
   uv venv
   source .venv/bin/activate  # Sous Windows : .venv\Scripts\activate
   ```

3. **Installer les dépendances**
   ```bash
   uv sync
   ```

4. **Configurer les variables d’environnement**
   ```bash
   cp .env.example .env
   # Éditez .env pour ajouter GOOGLE_API_KEY et CEREBRAS_API_KEY
   ```

---

## 4. Pipeline de données

### 4.1 Ingestion des PDF vers JSON (optionnel)

Si vous disposez déjà de fichiers JSON prêts dans `data/processed/`, vous pouvez passer cette étape.

```bash
uv run python ingest.py \
  --input-dir documents \
  --output-dir data/processed \
  --workers 4
```

- Chaque PDF est analysé par Docling pour produire un JSON structuré comprenant :
  - `content` : texte aplati pour l’embedding.
  - Des listes et tableaux par section (p. ex. _Caractéristiques produit_, _Données électriques_).
  - Des métadonnées alignées avec les filtres d’indexation.
- Chaque fichier JSON est enregistré dans `data/processed/<nom_fichier>.json`.

### 4.2 Schéma des JSON traités

Un fichier JSON représentatif contient :

```json
{
  "source": "documents/ZMP_1004795.pdf",
  "content": "Contenu textuel non formaté...",
  "Product features and benefits": ["Robust construction", "Consistent color"],
  "Areas of application": ["Stage & Theatre", "Studio"],
  "General Product Information": {
    "Product number (Americas)": "",
    "Product name (Americas)": "",
    "Family brand": "",
    "ANSI code": "FRJ"
  },
  "Electrical Data": {
    "Nominal wattage": "500W",
    "Nominal voltage": "240 V"
  },
  "...": "..."
}
```

Lors de l’indexation, les champs imbriqués sont aplatis (ex. `general_product_information`) afin d’autoriser des filtres par sous-chaîne.

---

## 5. Construction de l’index vectoriel

Vous pouvez construire l’index Chroma soit via l’entrée module, soit via l’enveloppe CLI de `main.py`.

### Option A : Appel direct du module

```bash
uv run python -m rag_mvp.index_json \
  --processed-dir data/processed \
  --index-dir data/index/chroma \
  --collection rag_mvp
```

### Option B : Via `main.py`

```bash
uv run python main.py index \
  --processed-dir data/processed \
  --index-dir data/index/chroma \
  --collection rag_mvp
```

Ces deux commandes :

- Vérifient l’existence des dossiers (`data/processed/`, `data/index/chroma/`).
- Chargent chaque document JSON, aplatissent les métadonnées et génèrent des embeddings avec `models/gemini-embedding-001` (requiert `GOOGLE_API_KEY`).
- Persistant les vecteurs dans la collection Chroma (`rag_mvp` par défaut).

La sortie console indique le nombre de documents indexés.

---

## 6. Utilisation de l’agent de chat

L’agent nécessite `GOOGLE_API_KEY` (pour la récupération) et `CEREBRAS_API_KEY` (pour le LLM).

### Option A : Point d’entrée module

```bash
uv run python -m rag_mvp.agent \
  --index-dir data/index/chroma \
  --collection rag_mvp
```

### Option B : Via `main.py`

Démarrer une session de chat directement :
```bash
uv run python main.py chat \
  --index-dir data/index/chroma \
  --collection rag_mvp
```

Indexer puis chatter en une seule étape :
```bash
uv run python main.py run \
  --processed-dir data/processed \
  --index-dir data/index/chroma \
  --collection rag_mvp
```

Une fois l’agent lancé :

- Posez des questions sur les spécifications produit.
- L’agent **doit** appeler l’outil de récupération avant de répondre ; il peut réessayer avec d’autres filtres.
- Les réponses incluent des citations comme `[1]` renvoyant aux documents consultés.
- Utilisez `exit` ou `quit` pour quitter la session.

### Filtres de récupération

L’invite de l’agent encourage des filtres de métadonnées tels que :

- `general_product_information` contient `ANSI code: FRJ`
- `physical_attributes_dimensions` contient `GY9.5`
- `areas_of_application` contient `Stage & Theatre`

Ces filtres permettent de cibler précisément les documents retournés.

---

## 7. Variables d’environnement

Ajoutez les éléments suivants à `.env` (chargé automatiquement via `dotenv` dans `main.py`) :

```dotenv
GOOGLE_API_KEY=your-google-key
CEREBRAS_API_KEY=your-cerebras-key
```

Variables optionnelles (à ajuster selon vos besoins) :

- `PROCESSED_DIR`, `INDEX_DIR`, `COLLECTION_NAME` – pour surcharger les valeurs par défaut dans vos scripts.

Assurez-vous que `.env` **n’est pas** versionné (déjà ignoré par `.gitignore`).

---

## 8. Dépannage

| Symptôme | Vérifications |
| --- | --- |
| Commande `uv` introuvable | Installer `uv` (https://github.com/astral-sh/uv). |
| "Missing embeddings" / erreurs avec les modèles Google | Vérifier que `GOOGLE_API_KEY` est défini et valide. |
| Échecs d’authentification Cerebras | Confirmer que `CEREBRAS_API_KEY` est exporté. |
| Aucune recherche ne renvoie de résultats | Vérifier que `data/processed/` contient des JSON avec un `content`