# Desktop Agent

Autonomous desktop automation agent with semantic understanding and memory graph learning.

**Status**: Production Ready (v1.0)

---

## What It Does

The Desktop Agent autonomously completes desktop tasks by:

1. **Observing** - Captures screen, extracts text with OCR
2. **Planning** - Uses LLM (NVIDIA Qwen) to decide next action
3. **Validating** - Checks action is safe before execution
4. **Executing** - Clicks, types, presses keys safely
5. **Verifying** - Confirms action had desired effect
6. **Learning** - Stores workflow patterns in memory graph

## Example Task

**Task**: "Open Chrome and search latest AI news"

```
[1] Observe: Desktop visible, no Chrome
[2] Plan: LLM decides to open Chrome
[3] Execute: Launches Chrome via subprocess
[4] Verify: Chrome window appears
[5] Plan: LLM decides to navigate to Google
[6] Execute: Opens Google search
[7] Plan: LLM decides to type search query
[8] Execute: Types "latest AI news" in search box
[9] Verify: Search results appear
[10] Goal Check: Keywords found → Task complete
```

**Total Time**: 5-10 seconds per loop, typically 3-5 loops to complete

---

## Architecture

See [assets/ARCHITECTURE.md](assets/ARCHITECTURE.md) for complete design documentation.

**Key Components**:
- `core/` - Agent loop, planning, execution
- `perception/` - Vision, OCR, UI element extraction
- `memory/` - Workflow memory graph, persistent storage
- `actions/` - Desktop control (click, type, window management)
- `llm/` - LLM integration (NVIDIA Qwen)
- `tests/` - Test suite

---

## Installation

### Requirements

- Python 3.8+
- Windows OS (tested on Windows 10/11)
- Tesseract OCR

### Setup

#### 1. Clone Repository
```bash
cd c:\Users\exeja\Desktop\Desktop-Agent
```

#### 2. Create Virtual Environment
```bash
python -m venv .venv
.venv\Scripts\activate
```

#### 3. Install Tesseract OCR

**Windows**:
- Download installer: https://github.com/UB-Mannheim/tesseract/wiki
- Install to: `C:\Program Files\Tesseract-OCR`
- Verify: `tesseract --version`

#### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

#### 5. Set API Keys

Create `.env` file in project root:
```
NVIDIA_API_KEY=your-nvidia-api-key
GEMINI_API_KEY=your-gemini-api-key
```

Get keys from:
- NVIDIA: https://build.nvidia.com/
- Gemini: https://ai.google.dev/

---

## Usage

### Run Agent

```bash
python main.py
```

This starts the main autonomous loop for the default task: "Open Chrome and search latest AI news"

### Run Tests

```bash
# Full test suite
python tests/workflow_test.py

# OCR test
python tests/ocr_test.py

# Vision test
python tests/vision_test.py

# Click test
python tests/click_test.py
```

### Stop Agent

Press **ESC** key to stop the agent immediately.

---

## Configuration

### Task Definition

Edit `desktop_agent/core/loop_agent.py`:
```python
def run_agent(task="Open Chrome and search latest AI news"):
    # Your task here
    pass
```

Or call with custom task:
```python
from desktop_agent.core.loop_agent import run_agent
run_agent("Your custom task here")
```

### Logging

Logs are displayed in terminal with colors:
- 🔵 OBSERVE (Blue)
- 🟣 PLAN (Magenta)  
- 🟢 EXECUTE (Green)
- 🔵 VERIFY (Cyan)
- 🟡 ACTION (Yellow)

Optional file logging in `agent.log`.

### Behavior Tuning

Edit `desktop_agent/core/loop_agent.py`:
```python
MAX_RETRIES = 5              # Max retry attempts
LOOP_COOLDOWN = 2            # Seconds between loops
ACTION_TIMEOUT = 3           # Seconds after action
```

---

## Project Structure

```
desktop_agent/
├── core/                # Agent loop & logic
│   ├── loop_agent.py   # Main autonomous loop
│   ├── observer.py     # Screen capture
│   ├── planner.py      # LLM planning
│   ├── executor.py     # Action execution
│   ├── validator.py    # Pre-execution checks
│   ├── verifier.py     # Outcome verification
│   ├── goal_checker.py # Task completion
│   ├── logger.py       # Logging system
│   └── state.py        # Agent state
│
├── perception/         # Vision & OCR
│   ├── vision.py       # Screenshot
│   ├── ocr_reader.py   # Text extraction
│   ├── ui_map.py       # UI elements
│   ├── click_text.py   # Semantic clicking
│   └── state_classifier.py
│
├── memory/             # Workflow memory
│   ├── memory_graph.py      # State graph
│   ├── memory_store.py      # SQLite storage
│   └── workflow_memory.py   # Pattern learning
│
├── actions/            # Desktop control
│   ├── actions.py           # Click, type, etc
│   ├── window_manager.py    # Focus management
│   └── app_map.py           # App launchers
│
├── llm/                # LLM integration
│   ├── agent.py        # NVIDIA Qwen client
│   └── config.py       # API config
│
└── tests/              # Test suite
    ├── workflow_test.py
    ├── ocr_test.py
    ├── vision_test.py
    └── click_test.py
```

---

## Supported Actions

The agent can execute these actions:

```python
{
    "action": "open_app",
    "app": "chrome"
}

{
    "action": "open_website",
    "url": "https://www.google.com"
}

{
    "action": "type",
    "text": "search query"
}

{
    "action": "press",
    "key": "enter"
}

{
    "action": "wait",
    "seconds": 2
}

{
    "action": "click",
    "x": 100,
    "y": 200
}

{
    "action": "click_text",
    "text": "Search"
}

{
    "action": "done"
}
```

---

## Reliability Features

✓ **Window Focus Management** - Ensures Chrome focused before typing  
✓ **Action Validation** - Pre-execution checks all parameters  
✓ **Retry Logic** - Retries failed actions up to 5 times  
✓ **Error Handling** - Graceful failure, detailed logs  
✓ **Verification** - Confirms screen changed as expected  
✓ **Emergency Stop** - ESC key to stop immediately  
✓ **Memory Tracking** - Stores workflows for learning  

---

## Logging

All actions are logged with timestamps and colors:

```
[12:30:01] OBSERVE
[12:30:03] Current state: google_search_page
[12:30:04] PLAN
[12:30:05] LLM returned action: type
[12:30:05] ACTION: type(latest AI news)
[12:30:07] EXECUTE
[12:30:08] Typing into Chrome: latest AI news...
[12:30:09] ✓ SUCCESS: Typed 17 characters
[12:30:10] VERIFY
[12:30:11] Verification: SUCCESS (screen changed, 78.0% similar)
```

---

## Performance

- **Loop Cycle**: 3-5 seconds
  - Screenshot: ~1s
  - OCR: ~1s
  - LLM: ~1-2s
  - Execute: <1s
  
- **Task Completion**: 5-10 loops
  - Simple search: 20-50 seconds total
  - Complex task: 1-2 minutes

---

## Troubleshooting

### Tesseract Not Found
```
Error: tesseract is not installed
```
**Fix**: Install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki

### API Keys Invalid
```
Error: Invalid API key for NVIDIA
```
**Fix**: Check `.env` file has correct keys from build.nvidia.com

### Chrome Not Focusing
```
Warning: Could not focus Chrome window
```
**Fix**: Ensure Chrome is installed and window title contains "Chrome"

### OCR Reading Nothing
```
Warning: OCR extracted 0 characters
```
**Fix**: Ensure screen is visible (not locked/screensaver)

---

## Memory System

### In-Memory Graph
- Stores state transitions
- Tracks successful workflows
- Used for pattern matching

### Persistent Storage
- SQLite database: `desktop_agent_memory.db`
- Stores states, actions, transitions
- Enables learning across runs

### Query Workflows
```python
from desktop_agent.memory.workflow_memory import workflow_memory

# Get similar successful workflows
similar = workflow_memory.get_similar_successful_workflows(
    ["state_chrome_open"],
    limit=3
)
```

---

## Future Roadmap

- ✅ Basic automation
- ✅ Memory graph
- ✅ Logging system
- ⏳ Workflow learning (in progress)
- ⏳ Multi-task orchestration
- ⏳ Remote execution
- ⏳ Advanced vision (object detection)

---

## Contributing

Improvements welcome! Areas for contribution:
- Better OCR preprocessing
- Additional app launchers in `app_map.py`
- More sophisticated state classification
- Workflow learning algorithms
- Performance optimization

---

## License

MIT License - See LICENSE file

---

## Support

For issues or questions:
1. Check logs: Look for error messages in terminal output
2. Run tests: `python tests/workflow_test.py`
3. Check assets/ARCHITECTURE.md for detailed design
4. Enable DEBUG logging for more details

---

## Version History

**v1.0** (May 12, 2026)
- Initial release
- Core loop working
- Memory graph implemented
- Comprehensive logging
- Production-ready

---

## Credits

Built with:
- NVIDIA Qwen LLM
- Tesseract OCR
- NetworkX (graph)
- PyAutoGUI (desktop control)
- Python 3.8+
