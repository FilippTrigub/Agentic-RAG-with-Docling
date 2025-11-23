# Agentic RAG MVP : Docling + LangChain + Chroma

Un système de génération augmentée par récupération (RAG) prêt pour la production qui recherche et interroge intelligemment la documentation produit structurée.

## Vue d'ensemble

Ce MVP démontre un pipeline RAG agentique qui :

1. **Analyse les documents** - Extrait des données structurées depuis les PDF avec Docling (tableaux, sections, métadonnées)
2. **Incorpore le contenu** - Génère des embeddings vectoriels via Google Generative AI
3. **Stocke de manière recherchable** - Persiste les embeddings et métadonnées dans Chroma avec des métadonnées filtrables
4. **Active la recherche intelligente** - Fournit un agent de chat avec des capacités RAG itératives
5. **Filtre avec précision** - Prend en charge les filtres exacts `where` et le filtrage post-récupération par sous-chaîne `contains`
6. **Maintient le contexte** - Préserve la mémoire de conversation à travers les interactions

### Fonctionnalités clés

- **Ingestion parallèle de documents** avec des processus de travail configurables
- **Extraction structurée de métadonnées** depuis les fiches techniques produit (spécifications techniques, fonctionnalités, applications)
- **Recherche hybride** combinant similarité vectorielle et filtrage de métadonnées
- **Récupération agentique** pouvant affiner itérativement les recherches
- **Attribution des sources** avec citations en ligne

## Prérequis

- **Python 3.13+** (gestion des dépendances via `uv`)
- **Clés API** :
  - Clé API Google Generative AI (pour les embeddings)
  - Clé API Cerebras (pour le modèle de chat)

## Démarrage rapide

### 1. Configuration de l'environnement

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
# GOOGLE_API_KEY=votre_cle_api_google
# CEREBRAS_API_KEY=votre_cle_api_cerebras
```

### 3. Préparer les données

Le dépôt inclut des fichiers JSON pré-traités dans `data/processed/`. Pour traiter vos propres PDF :

```bash
# Placer les PDF dans le répertoire documents/, puis exécuter :
uv run python ingest.py --input-dir documents --output-dir data/processed --workers 6
```

### 4. Exécuter l'application

**Option A : Tout-en-un** (indexation + chat)
```bash
uv run python main.py run
```

**Option B : Étape par étape**
```bash
# Construire l'index vectoriel
uv run python main.py index --processed-dir data/processed --index-dir data/index/chroma

# Démarrer l'agent de chat
uv run python main.py chat --index-dir data/index/chroma
```

## Architecture

### Pipeline de données

```
PDF → [Analyseur Docling] → JSON structuré → [Embeddings] → Chroma Vector Store → [Agent + Outils] → Utilisateur
```

### Format des données

Les fichiers JSON traités (`data/processed/`) suivent cette structure :

```json
{
  "source": "documents/product.pdf",
  "content": "Contenu texte complet...",
  "Product features and benefits": ["fonctionnalité 1", "fonctionnalité 2"],
  "Areas of application": ["application 1", "application 2"],
  "General Product Information": {
    "ANSI code": "ABC123",
    "Product name (Americas)": "Nom du produit"
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

Pendant l'indexation, le système ajoute un `doc_id` (dérivé du nom de fichier) et aplatit les métadonnées imbriquées pour un filtrage efficace.

### Transformation des métadonnées

Pendant l'indexation, les structures imbriquées sont aplaties en chaînes délimitées par des pipes pour le filtrage par sous-chaîne :

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

Cela permet une correspondance efficace de sous-chaînes sur les champs de métadonnées (par exemple, rechercher "GY9.5" dans les spécifications de base de lampe).

## Exemples d'utilisation

### Chat interactif

```bash
uv run python main.py chat --index-dir data/index/chroma
```

**Exemples de requêtes :**
- "Montrez-moi toutes les lampes avec une température de couleur de 3200K"
- "Quels sont les produits dimmables adaptés à la scène et au théâtre ?"
- "Trouvez des lampes avec base GY9.5 et puissance 500W"

L'agent :
- Récupère les documents pertinents en utilisant la similarité vectorielle
- Applique des filtres de métadonnées (clauses exactes `where` ou filtres de sous-chaîne `contains`)
- Affine itérativement les recherches si nécessaire
- Fournit des réponses avec des citations en ligne comme `[1]`, `[2]`

## Structure du projet

```
.
├── main.py                    # Point d'entrée CLI (commandes index, chat, run)
├── ingest.py                  # Ingestion PDF→JSON avec traitement parallèle
├── rag_mvp/
│   ├── index_json.py         # Constructeur d'index Chroma
│   ├── tools.py              # Outil de récupération avec filtrage de métadonnées
│   └── agent.py              # Agent de chat LangChain avec capacités RAG
├── data/
│   ├── processed/            # Fichiers JSON analysés (entrée pour l'indexation)
│   └── index/chroma/         # Persistance du magasin vectoriel Chroma
├── pyproject.toml            # Dépendances du projet (gérées par uv)
├── .env.example              # Modèle de variables d'environnement
└── README.md                 # Ce fichier
```

## Notes d'implémentation

### Décisions de conception

**Docling pour l'extraction** : Choisi pour ses capacités robustes d'analyse de tableaux. Bien que la cohérence des champs varie selon les documents (par exemple, identifiants de produit), l'approche de recherche large utilisant les filtres `where` et `contains` gère cela avec élégance.

**Aplatissement des métadonnées** : Les structures imbriquées sont aplaties en chaînes délimitées par des pipes, permettant des recherches de sous-chaînes sans langages de requête complexes.

**Approche agentique** : L'agent LangChain peut invoquer itérativement l'outil RAG, affinant les recherches basées sur les résultats initiaux.

### Limitations connues

- **Filtrage numérique** : Les métadonnées sont stockées sous forme de chaînes. L'implémentation de requêtes de plage (par exemple, "puissance > 100") nécessite une analyse et une indexation numérique structurée.
- **Sensibilité du modèle** : La génération de filtres dépend de l'interprétation du LLM. L'ingénierie des prompts et l'ajustement de la température peuvent améliorer la cohérence.
- **Variables globales** : L'implémentation actuelle utilise des globales pour la simplicité. Le déploiement en production nécessite une refactorisation pour la concurrence.

### Considérations d'échelle

**Pour le déploiement en production :**

1. **Magasin vectoriel** : Migrer de Chroma local vers des solutions hébergées (Qdrant, Pinecone, Weaviate)
2. **Couche API** : Implémenter la gestion asynchrone des requêtes avec FastAPI ou frameworks similaires
3. **Déploiement** : Conteneuriser avec Docker et déployer sur Kubernetes, ou utiliser du serverless (AWS Lambda, Cloud Run)
4. **Limitation des résultats** : Implémenter la pagination et des limites strictes pour éviter l'épuisement de la fenêtre de contexte
5. **Mise en cache** : Ajouter Redis/Memcached pour les requêtes fréquemment consultées
6. **Surveillance** : Intégrer l'observabilité (OpenTelemetry, Langfuse) pour le suivi de la latence et des coûts

**À grande échelle :**
- Les requêtes exhaustives ("donnez-moi tous les produits") deviennent impraticables en raison des limites de contexte et du coût
- Implémenter une synthèse intelligente des résultats et une divulgation progressive
- Considérer des architectures hybrides avec des bases de données traditionnelles pour les requêtes structurées

## Dépannage

### Problèmes courants

**Aucun embedding généré**
```bash
# S'assurer que GOOGLE_API_KEY est définie
echo $GOOGLE_API_KEY  # Linux/Mac
echo %GOOGLE_API_KEY% # Windows
```

**L'authentification Cerebras échoue**
```bash
# Vérifier CEREBRAS_API_KEY dans .env
cat .env | grep CEREBRAS_API_KEY
```

**Aucun résultat de recherche**
- Confirmer que `data/processed/` contient des fichiers JSON avec des champs `content` non vides
- Reconstruire l'index : `uv run python main.py index`
- Vérifier que le répertoire d'index existe et contient des données : `ls -la data/index/chroma/`

**Erreurs d'importation de module**
```bash
# Réinstaller les dépendances
uv sync --force
```

**L'ingestion parallèle échoue**
```bash
# Réduire le nombre de workers
uv run python ingest.py --workers 1
```

## Développement

### Ajouter des dépendances

```bash
uv add nom-du-package           # Ajouter une dépendance d'exécution
uv add --dev nom-du-package     # Ajouter une dépendance de développement
```

### Tests

```bash
# Installer pytest
uv add --dev pytest

# Exécuter les tests (lorsque disponibles)
uv run pytest
```

### Style de code

- Python 3.13+, directives de style PEP 8
- Indentation à 4 espaces
- Annotations de type préférées
- Docstrings pour les fonctions non triviales

Voir `AGENTS.md` pour les directives de développement détaillées.

## Contribution

1. Créer une branche de fonctionnalité
2. Apporter des modifications ciblées et progressives
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
