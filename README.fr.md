# Agentic RAG MVP : Docling + LangChain + Chroma

Un système de génération augmentée par récupération (RAG) prêt pour la production qui recherche et interroge intelligemment la documentation produit structurée.

## Présentation

Ce MVP démontre un pipeline RAG agentique qui :

1. **Analyse les documents** - Extrait des données structurées des PDF à l'aide de Docling (tableaux, sections, métadonnées)
2. **Génère des embeddings** - Crée des embeddings vectoriels via Google Generative AI
3. **Stocke de manière recherchable** - Persiste les embeddings et métadonnées dans Chroma avec des métadonnées filtrables
4. **Permet une recherche intelligente** - Fournit un agent conversationnel avec des capacités RAG itératives
5. **Filtre avec précision** - Prend en charge les filtres exacts `where` et le filtrage post-récupération par sous-chaînes `contains`
6. **Maintient le contexte** - Préserve la mémoire conversationnelle à travers les interactions

### Fonctionnalités Clés

- **Ingestion parallèle de documents** avec processus workers configurables
- **Extraction de métadonnées structurées** des fiches techniques produits (spécifications techniques, fonctionnalités, applications)
- **Recherche hybride** combinant similarité vectorielle et filtrage de métadonnées
- **Récupération agentique** capable d'affiner itérativement les recherches
- **Attribution des sources** avec citations en ligne

## Prérequis

- **Python 3.13+** (gestion des dépendances via `uv`)
- **Clés API** :
  - Clé API Google Generative AI (pour les embeddings)
  - Clé API Cerebras (pour le modèle de chat)

## Démarrage Rapide

### 1. Configuration de l'Environnement

```bash
# Créer et activer l'environnement virtuel
uv venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows

# Installer les dépendances
uv sync
```

### 2. Configuration

```bash
# Copier le modèle d'environnement et ajouter vos clés API
cp .env.example .env
# Éditer .env et ajouter :
# GOOGLE_API_KEY=votre_clé_api_google
# CEREBRAS_API_KEY=votre_clé_api_cerebras
```

### 3. Préparer les Données

Le dépôt inclut des fichiers JSON pré-traités dans `data/processed/`. Pour traiter vos propres PDF :

```bash
# Placer les PDF dans le répertoire documents/, puis exécuter :
uv run python ingest.py --input-dir documents --output-dir data/processed --workers 6
```

### 4. Lancer l'Application

**Option A : Tout-en-un** (indexation + chat)
```bash
uv run python main.py run
```

**Option B : Étape par étape**
```bash
# Construire l'index vectoriel
uv run python main.py index --processed-dir data/processed --index-dir data/index/chroma

# Démarrer l'agent conversationnel
uv run python main.py chat --index-dir data/index/chroma
```

## Architecture

### Pipeline de Données

```
PDFs → [Analyseur Docling] → JSON Structuré → [Embeddings] → Chroma Vector Store → [Agent + Outils] → Utilisateur
```

### Format de Données

Les fichiers JSON traités (`data/processed/`) suivent cette structure :

```json
{
  "source": "documents/product.pdf",
  "content": "Contenu textuel complet...",
  "Product features and benefits": ["fonctionnalité 1", "fonctionnalité 2"],
  "Areas of application": ["application 1", "application 2"],
  "General Product Information": {
    "ANSI code": "ABC123",
    "Product name (Americas)": "Nom du Produit"
  },
  "Electrical Data": {
    "Nominal wattage": "500W",
    "Nominal voltage": "240 V"
  },
  "Photometric Data": {
    "Nominal luminous flux": "13500 lm",
    "Color temperature": "3200 K"
  },
  "Physical Attributes & Dimensions": {
    "Lamp base": "GY9.5",
    "Diameter": "18.0mm"
  },
  "Operating Conditions": {
    "Burning position": "Any",
    "Dimmable": "Yes"
  },
  "Environmental & Regulatory Information": {
    "Energy efficiency class": "G"
  }
}
```

Durant l'indexation, le système ajoute un `doc_id` (dérivé du nom de fichier) et aplatit les métadonnées imbriquées pour un filtrage efficace.

### Transformation des Métadonnées

Durant l'indexation, les structures imbriquées sont aplaties en chaînes délimitées par des pipes pour le filtrage par sous-chaînes :

```json
{
  "doc_id": "ZMP_1004795",
  "source": "documents\\ZMP_1004795.pdf",
  "areas_of_application": "Stage & Theatre | Studio, TV, & Film | Professional Photography | Club & Disco",
  "electrical_data": "Nominal wattage: 500W | Nominal voltage: 240 V",
  "photometric_data": "Nominal luminous flux: 13500 lm | Color temperature: 3200 K | ...",
  "product_features_and_benefits": "Robust construction | Consistent color | Dimmable to 0%",
  "physical_attributes_dimensions": "Lamp base: GY9.5 | Diameter: 18.0mm | Length: 80.0mm"
}
```

Cela permet une correspondance efficace de sous-chaînes sur les champs de métadonnées (par exemple, recherche de "GY9.5" dans les spécifications de culot de lampe).

## Exemples d'Utilisation

### Chat Interactif

```bash
uv run python main.py chat --index-dir data/index/chroma
```

**Exemples de requêtes :**
- "Montrez-moi toutes les lampes avec une température de couleur de 3200K"
- "Quels sont les produits dimmables adaptés à la scène et au théâtre ?"
- "Trouvez les lampes avec culot GY9.5 et puissance 500W"

L'agent :
- Récupère les documents pertinents en utilisant la similarité vectorielle
- Applique les filtres de métadonnées (clauses `where` exactes ou filtres `contains` par sous-chaînes)
- Affine itérativement les recherches si nécessaire
- Fournit des réponses avec des citations en ligne comme `[1]`, `[2]`

## Structure du Projet

```
.
├── main.py                    # Point d'entrée CLI (commandes index, chat, run)
├── ingest.py                  # Ingestion PDF→JSON avec traitement parallèle
├── rag_mvp/
│   ├── index_json.py         # Constructeur d'index Chroma
│   ├── tools.py              # Outil de récupération avec filtrage de métadonnées
│   └── agent.py              # Agent conversationnel LangChain avec capacités RAG
├── data/
│   ├── processed/            # Fichiers JSON analysés (entrée pour l'indexation)
│   └── index/chroma/         # Persistance du vector store Chroma
├── pyproject.toml            # Dépendances du projet (gérées par uv)
├── .env.example              # Modèle de variables d'environnement
└── README.md                 # Ce fichier
```

## Notes d'Implémentation

### Décisions de Conception

**Docling pour l'Extraction** : Choisi pour ses capacités robustes d'analyse de tableaux. Bien que la cohérence des champs varie selon les documents (par exemple, identifiants de produits), l'approche de recherche large utilisant les filtres `where` et `contains` gère cela avec élégance.

**Aplatissement des Métadonnées** : Les structures imbriquées sont aplaties en chaînes délimitées par pipes, permettant des recherches par sous-chaînes sans langages de requête complexes.

**Approche Agentique** : L'agent LangChain peut invoquer itérativement l'outil RAG, affinant les recherches en fonction des résultats initiaux.

### Limitations Connues

- **Filtrage numérique** : Les métadonnées sont stockées sous forme de chaînes. L'implémentation de requêtes par plage (par exemple, "puissance > 100") nécessite une analyse et une indexation numérique structurée.
- **Sensibilité du modèle** : La génération de filtres dépend de l'interprétation du LLM. L'ingénierie de prompts et l'ajustement de la température peuvent améliorer la cohérence.
- **Variables globales** : L'implémentation actuelle utilise des variables globales par simplicité. Un déploiement en production nécessite une refactorisation pour la concurrence.

### Considérations d'Échelle

**Pour un déploiement en production :**

1. **Vector Store** : Migrer de Chroma local vers des solutions hébergées (Qdrant, Pinecone, Weaviate)
2. **Couche API** : Implémenter la gestion asynchrone des requêtes avec FastAPI ou frameworks similaires
3. **Déploiement** : Conteneuriser avec Docker et déployer sur Kubernetes, ou utiliser serverless (AWS Lambda, Cloud Run)
4. **Limitation des Résultats** : Implémenter la pagination et des limites strictes pour éviter l'épuisement de la fenêtre de contexte
5. **Cache** : Ajouter Redis/Memcached pour les requêtes fréquemment consultées
6. **Surveillance** : Intégrer l'observabilité (OpenTelemetry, Langfuse) pour le suivi de la latence et des coûts

**À grande échelle :**
- Les requêtes exhaustives ("donnez-moi tous les produits") deviennent impraticables en raison des limites de contexte et du coût
- Implémenter une synthèse intelligente des résultats et une divulgation progressive
- Envisager des architectures hybrides avec des bases de données traditionnelles pour les requêtes structurées

## Dépannage

### Problèmes Courants

**Aucun embedding généré**
```bash
# S'assurer que GOOGLE_API_KEY est définie
echo $GOOGLE_API_KEY  # Linux/Mac
echo %GOOGLE_API_KEY% # Windows
```

**Échec d'authentification Cerebras**
```bash
# Vérifier CEREBRAS_API_KEY dans .env
cat .env | grep CEREBRAS_API_KEY
```

**Aucun résultat de recherche**
- Confirmer que `data/processed/` contient des fichiers JSON avec des champs `content` non vides
- Reconstruire l'index : `uv run python main.py index`
- Vérifier que le répertoire d'index existe et contient des données : `ls -la data/index/chroma/`

**Erreurs d'importation de modules**
```bash
# Réinstaller les dépendances
uv sync --force
```

**Échec de l'ingestion parallèle**
```bash
# Réduire le nombre de workers
uv run python ingest.py --workers 1
```

## Développement

### Ajout de Dépendances

```bash
uv add nom-du-package           # Ajouter une dépendance d'exécution
uv add --dev nom-du-package     # Ajouter une dépendance de développement
```

### Tests

```bash
# Installer pytest
uv add --dev pytest

# Exécuter les tests (si disponibles)
uv run pytest
```

### Style de Code

- Python 3.13+, directives de style PEP 8
- Indentation de 4 espaces
- Indices de type préférés
- Docstrings pour les fonctions non triviales

Voir `AGENTS.md` pour des directives de développement détaillées.

## Contribution

1. Créer une branche de fonctionnalité
2. Effectuer des modifications ciblées et incrémentales
3. Mettre à jour le README si le comportement change
4. Utiliser des commits conventionnels (par exemple, `feat:`, `fix:`, `docs:`)
5. Ouvrir une pull request avec une description claire

## Licence

[Spécifiez votre licence ici]

## Remerciements

- **Docling** - Analyse de documents et extraction de structure
- **LangChain** - Framework RAG agentique
- **Chroma** - Base de données vectorielle
- **Google Generative AI** - Embeddings
- **Cerebras** - Inférence rapide pour le modèle de chat
