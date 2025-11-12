# 🚀 Quick Start: Funky RAG MVP

## Installation

1. **Install dependencies:**
```bash
pip install rich python-dotenv langchain langchain-cerebras langchain-community \
            langchain-core langchain-google-genai chromadb jq
```

Or if using `uv`:
```bash
uv sync
```

2. **Set up environment:**
```bash
cp .env.example .env
# Edit .env and add your API keys:
# - GOOGLE_API_KEY (for embeddings)
# - CEREBRAS_API_KEY (for LLM)
```

## Usage

### 🎨 See the Funky Banner
```bash
python3 main.py --help
```

### 📚 Index Your Documents
```bash
python3 main.py index
```

This will:
- Show animated progress bars 📊
- Display colorful status messages ✨
- Create a beautiful success panel 🎉

### 💬 Start Chatting
```bash
python3 main.py chat
```

Features:
- Styled welcome panel 🤖
- Emoji-enhanced prompts 💬
- Beautiful response panels 📦
- Source tables 📚
- Friendly exit messages 👋

### 🚀 Do Both (Index + Chat)
```bash
python3 main.py run
```

### 🎭 Test the Funky Features
```bash
python3 test_funky.py
```

This demo shows all the visual enhancements without needing API keys!

## Commands Reference

| Command | Description | Emoji |
|---------|-------------|-------|
| `main.py --help` | Show help with banner | 🎨 |
| `main.py index` | Index documents | 📚 |
| `main.py chat` | Start chat | 💬 |
| `main.py run` | Index + Chat | 🚀 |
| `test_funky.py` | Demo features | 🎭 |

## Emoji Guide

| Emoji | Meaning |
|-------|---------|
| 🚀 | Launch/Start |
| 📚 | Indexing |
| 💬 | Chat |
| 🤖 | AI Assistant |
| 🔍 | Searching |
| ✨ | Success/Magic |
| 🎉 | Celebration |
| 📁 | Files |
| 💾 | Database |
| 🔮 | Processing |
| 📊 | Progress |
| 👋 | Goodbye |
| ⚠️ | Warning |
| ❌ | Error |

## Color Scheme

- **Cyan** - Information, headers
- **Green** - Success, positive actions
- **Yellow** - Highlights, important values
- **Magenta** - Section headers, user input
- **Red** - Errors, warnings
- **Blue** - Tables, borders
- **Dim** - Secondary information

## Tips

1. **Terminal Support**: Works best in modern terminals that support:
   - 256 colors
   - Unicode characters
   - ANSI escape codes

2. **Best Experience**: Use terminals like:
   - iTerm2 (macOS)
   - Windows Terminal (Windows)
   - GNOME Terminal (Linux)
   - VS Code integrated terminal

3. **Troubleshooting**:
   - If colors don't show: Check terminal color support
   - If emojis are broken: Update terminal font
   - If progress bars glitch: Ensure terminal width > 80 chars

## Examples

### Quick Index
```bash
python3 main.py index --processed-dir data/processed --index-dir data/index/chroma
```

### Chat with Custom Collection
```bash
python3 main.py chat --index-dir data/index/chroma --collection my_docs
```

### Full Pipeline
```bash
python3 main.py run --processed-dir data/processed --index-dir data/index/chroma
```

## What Makes It Funky? 🎨

1. **ASCII Art Banner** - Eye-catching header
2. **Progress Bars** - Visual feedback for long operations
3. **Colored Output** - Easy to scan and understand
4. **Emojis** - Fun and informative
5. **Styled Panels** - Professional presentation
6. **Tables** - Organized data display
7. **Animations** - Spinners and progress indicators

## Next Steps

1. Try the demo: `python3 test_funky.py`
2. Index your documents: `python3 main.py index`
3. Start chatting: `python3 main.py chat`
4. Enjoy the funky experience! 🎉

---

**Have fun with your funky RAG MVP!** ✨🚀
