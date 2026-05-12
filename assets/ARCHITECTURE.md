# Desktop Agent Architecture

**Version**: 1.0  
**Date**: May 12, 2026  
**Status**: Refactored & Production-Ready

---

## Overview

The Desktop Agent is a **reliable autonomous desktop automation system** that operates in closed-loop cycles:

```
OBSERVE → PLAN → VALIDATE → EXECUTE → VERIFY → MEMORY
```

The system maintains semantic memory of workflows, learns from successful patterns, and implements deterministic execution with comprehensive logging.

---

## Project Structure

```
desktop_agent/
│
├── core/                    # Agent loop & core logic
│   ├── loop_agent.py       # Main observe-plan-execute-verify loop
│   ├── observer.py         # Environment perception
│   ├── planner.py          # LLM action planning
│   ├── executor.py         # Safe action execution with focus mgmt
│   ├── verifier.py         # Outcome verification
│   ├── validator.py        # Pre-execution validation
│   ├── goal_checker.py     # Task completion detection
│   ├── state.py            # Agent state dict
│   ├── logger.py           # Logging system (colored, timestamped)
│   └── __init__.py
│
├── perception/             # Vision & UI understanding
│   ├── vision.py          # Screenshot capture
│   ├── ocr_reader.py      # Tesseract OCR extraction
│   ├── ui_map.py          # UI element extraction
│   ├── text_locator.py    # Text position finding
│   ├── click_text.py      # Semantic text clicking
│   ├── state_classifier.py # Screen state classification
│   ├── environment_state.py
│   └── __init__.py
│
├── memory/                 # Workflow memory & graph
│   ├── memory_graph.py    # NetworkX-based state graph
│   ├── memory_store.py    # SQLite persistent storage
│   ├── workflow_memory.py # Learned workflow tracking
│   └── __init__.py
│
├── actions/                # Desktop automation
│   ├── actions.py         # Click, type, press, wait, open
│   ├── app_map.py         # App name to command mapping
│   ├── window_manager.py  # Window focus management
│   └── __init__.py
│
├── llm/                    # LLM integration
│   ├── agent.py           # NVIDIA Qwen API client
│   ├── config.py          # API keys & config
│   └── __init__.py
│
└── tests/                  # Test suite
    ├── workflow_test.py   # Full workflow tests
    ├── ocr_test.py        # OCR validation
    ├── click_test.py      # Click action tests
    ├── vision_test.py     # Vision capture tests
    └── window_test.py     # Window management tests
```

---

## Core Modules

### 1. Core Loop (`core/loop_agent.py`)

**Responsibility**: Main autonomous agent loop

**Flow**:
```
1. OBSERVE: Capture screen, extract text/UI
2. CHECK GOAL: Is task complete?
3. PLAN: Ask LLM for next action
4. VALIDATE: Is action safe/possible?
5. EXECUTE: Run action with focus management
6. VERIFY: Did screen change as expected?
7. RETRY: Max 5 retries on failure
8. MEMORY: Log to graph & persistent store
```

**Key Features**:
- Loop count tracking
- Max retry logic (5 retries before stopping)
- Emergency ESC key stop
- Comprehensive logging at each stage
- Workflow memory integration

### 2. Observer (`core/observer.py`)

**Responsibility**: Perceive current environment

**Captures**:
- Screenshot → `vision.py`
- OCR text → `ocr_reader.py`
- UI elements → `ui_map.py`

**Returns**:
```python
{
    "image": "screen.png",
    "text": "Google Search\nLatest AI News",
    "elements": [
        {"text": "Search", "x": 100, "y": 200},
        {"text": "Google", "x": 50, "y": 50}
    ]
}
```

### 3. Planner (`core/planner.py`)

**Responsibility**: Plan next action using LLM

**Inputs**:
- Task description
- Current screen text
- Agent state

**LLM**: NVIDIA Qwen (qwen3-coder-480b-a35b-instruct)

**Output**: Single action
```python
{
    "action": "type",
    "text": "latest AI news"
}
```

**Fallback**: Wait 2 seconds if LLM fails

### 4. Executor (`core/executor.py`)

**Responsibility**: Execute actions safely

**Safety Features**:
- Window focus management (ensures Chrome is active)
- Action validation before execution
- Error handling with logging
- Cooldown between actions (0.5s)

**Supported Actions**:
```
- open_app(app)      # Launch application
- open_website(url)  # Open URL in browser
- type(text)         # Type text (with focus verification)
- press(key)         # Press keyboard key
- wait(seconds)      # Wait before next action
- click(x, y)        # Click at coordinates
- click_text(text)   # Find and click text on screen
- done               # Mark task complete
```

### 5. Validator (`core/validator.py`)

**Responsibility**: Pre-execution safety check

**Validates**:
- Action type is allowed
- Required parameters present
- Parameter types correct
- Values in acceptable ranges

**Example Validations**:
- `click_text`: Target text exists on screen
- `type`: Text not empty
- `click`: Coordinates numeric & valid
- `wait`: Duration 0-60 seconds

### 6. Verifier (`core/verifier.py`)

**Responsibility**: Verify action execution success

**Compares**:
- Screen text before/after
- UI elements changed
- Calculates similarity %

**Returns**:
```python
{
    "success": True,
    "similarity": 0.72,
    "changed": True
}
```

### 7. Goal Checker (`core/goal_checker.py`)

**Responsibility**: Detect task completion

**Patterns**:
- "latest ai news" → looks for keywords (ai, news, results)
- "open chrome" → checks for Chrome indicators
- "search" → checks for result indicators

---

## Perception Pipeline

### Vision (`perception/vision.py`)
- Captures screenshot using PyAutoGUI
- Saves to `screen.png`

### OCR (`perception/ocr_reader.py`)
- Tesseract OCR (local, no cloud)
- Extracts all visible text from screen

### UI Map (`perception/ui_map.py`)
- Extracts UI element bounding boxes
- Returns text + coordinates for clickable items

### Text Locator (`perception/text_locator.py`)
- Finds specific text on screen
- Returns pixel coordinates

### Click Text (`perception/click_text.py`)
- Semantic text clicking
- Finds text and clicks its center
- Most reliable interaction method

### State Classifier (`perception/state_classifier.py`)
- Classifies current UI state (e.g., "chrome_open", "search_results")
- Used for memory graph nodes

---

## Memory System

### Memory Graph (`memory/memory_graph.py`)

**Technology**: NetworkX DiGraph (directed graph)

**Stores**:
```
Nodes (States):
  - "state_chrome_open" (semantic, not raw text)
  - "state_google_loaded"
  - "state_search_results"

Edges (Transitions):
  - state → action → state
  - Metadata: action type, outcome
```

**Queries**:
- `query_similar_paths(start, end)` → Find workflow paths
- Path analysis for workflow learning

### Memory Store (`memory/memory_store.py`)

**Technology**: SQLite (persistent local storage)

**Tables**:
- `states`: Semantic UI states
- `actions`: Executed actions
- `transitions`: State changes
- `workflows`: Learned successful workflows

**Queries**:
- `store_state()`: Save state
- `store_action()`: Log action
- `record_transition()`: Track workflow
- `get_recent_transitions()`: Query history
- `query_similar_states()`: Find similar past states

### Workflow Memory (`memory/workflow_memory.py`)

**Tracks**:
- Current workflow states
- Current workflow actions
- Success/failure metrics

**Learns**:
- Successful workflow patterns
- State transitions that work
- Best next action suggestions

---

## Actions System

### Actions (`actions/actions.py`)

**Implemented Actions**:
```python
open_app(app_name)           # Launch app
open_website(url)            # Open URL
type_text(text)              # Type with 30ms interval
press_key(key)               # Press key (Enter, Tab, etc)
wait(seconds)                # Wait
click(x, y)                  # Direct click
```

**Error Handling**:
- Try/catch around each action
- Logs success/failure
- Safe errors don't crash loop

### Window Manager (`actions/window_manager.py`)

**Features**:
- `get_active_window()` → Get current focused window title
- `focus_window(keyword)` → Focus window by partial match
- Critical for `type` actions (must focus Chrome)

### App Map (`actions/app_map.py`)

**Maps**:
```python
"chrome" → "start chrome"
"firefox" → "start firefox"
"notepad" → "notepad"
```

Platform-specific launcher commands.

---

## Logging System

### Logger (`core/logger.py`)

**Features**:
- Timestamped [HH:MM:SS] format
- Colored output (terminal)
- Optional file logging
- Log levels: DEBUG, INFO, WARNING, ERROR

**Colored Sections**:
- OBSERVE (Blue)
- PLAN (Magenta)
- EXECUTE (Green)
- VERIFY (Cyan)
- ACTION (Yellow)

**Usage**:
```python
from desktop_agent.core.logger import logger, log_section, log_action

logger.info("Starting task")
log_section("OBSERVE")
log_action("click_text", "Search")
log_result(True, "Successfully clicked search")
```

**Example Output**:
```
[12:30:01] INFO     Starting agent with task: Open Chrome and search latest AI news
[12:30:02] INFO     OBSERVE
[12:30:03] DEBUG    Screen text (first 100 chars): Google Search Chrome
[12:30:03] INFO     Current state: google_search_page
[12:30:04] INFO     PLAN
[12:30:05] INFO     LLM returned action: type
[12:30:05] INFO     ACTION: type(latest AI news)
[12:30:07] INFO     EXECUTE
[12:30:08] INFO     Typing into Chrome: latest AI news...
[12:30:09] INFO     ✓ SUCCESS: Typed 17 characters
```

---

## LLM Integration

### Agent (`llm/agent.py`)

**Provider**: NVIDIA API (integrate.api.nvidia.com)

**Model**: qwen3-coder-480b-a35b-instruct

**Parameters**:
- Temperature: 0.2 (deterministic)
- Top-p: 0.8
- Max tokens: 1024
- Timeout: 30 seconds

**Prompt Structure**:
```
[System]: You are a desktop automation AI. Return ONLY valid JSON.

[User]: 
Task: Open Chrome and search latest AI news
Current screen text: [OCR result]
Current state: {agent_state}
Rules: [behavioral rules]
```

**Response**:
```json
{
  "actions": [{
    "action": "type",
    "text": "latest AI news"
  }]
}
```

**Fallback**: If LLM fails, returns `{"actions": [{"action": "wait", "seconds": 2}]}`

---

## Execution Flow Example

### Task: "Open Chrome and search latest AI news"

**Loop 1: Initial State**
```
[OBSERVE] Screen: Desktop, no Chrome
[GOAL_CHECK] Not complete
[PLAN] LLM: open_app(chrome)
[VALIDATE] open_app is allowed ✓
[EXECUTE] subprocess.Popen("start chrome")
[VERIFY] No visible change yet (Chrome launching)
[MEMORY] state_desktop → action_open_chrome → state_chrome_loading
```

**Loop 2: Chrome Open**
```
[OBSERVE] Screen: Chrome opened, address bar visible
[GOAL_CHECK] Not complete
[PLAN] LLM: open_website(https://www.google.com)
[VALIDATE] URL valid ✓
[EXECUTE] webbrowser.open(url)
[VERIFY] Screen changed, Google load page visible
[MEMORY] state_chrome_loading → action_open_google → state_google_loading
```

**Loop 3: Google Loaded**
```
[OBSERVE] Screen: Google search page
[GOAL_CHECK] Not complete
[PLAN] LLM: click_text("search box") OR type("latest AI news")
[VALIDATE] "search box" found on screen ✓
[EXECUTE] click_text(search_box) focuses input, then types
[VERIFY] Search text entered, can see query in box
[MEMORY] state_google_search → action_search_click → state_search_input
```

**Loop 4: Search**
```
[OBSERVE] Screen: Search results with AI news
[GOAL_CHECK] Check keywords: "search results" + "ai news" ✓ COMPLETE
[MEMORY] state_search_input → action_press_enter → state_search_results
[PRINT_GRAPH] Workflow stored
[EXIT]
```

---

## Configuration

### Environment Variables

```bash
NVIDIA_API_KEY=your-api-key-here
GEMINI_API_KEY=your-gemini-key-here
```

### State File

Agent state persists in memory:
```python
state = {
    "retries": 0,
    "last_success": None,
    "chrome_opened": False,
    "max_retries": 5
}
```

---

## Reliability Features

### 1. Focus Management
- Always focus Chrome before typing
- Verify window is active
- Fallback to alternative focus methods

### 2. Validation Pipeline
- Pre-execution check all parameters
- Verify text exists before click_text
- Block invalid coordinates

### 3. Retry Logic
- Track failures per action
- Max 5 retries before stopping
- Reset counter on success

### 4. Error Handling
- Try/catch around every action
- Logged exceptions with stack traces
- Graceful failures (wait instead of crash)

### 5. Verification
- Screen comparison before/after
- Similarity scoring
- Detect if action had no effect

### 6. Emergency Stop
- ESC key stops agent immediately
- Graceful shutdown logging
- No orphaned processes

---

## Testing

### Test Suite

```bash
# Memory graph functionality
python tests/workflow_test.py --test memory_graph

# Workflow memory
python tests/workflow_test.py --test workflow_memory

# Simple click
python tests/workflow_test.py --test simple_click

# Full search workflow (manual)
python tests/workflow_test.py --test search_workflow
```

### OCR Test
```bash
python tests/ocr_test.py
```
Captures screen and reads text.

### Vision Test
```bash
python tests/vision_test.py
```
Captures and saves screenshot.

### Click Test
```bash
python tests/click_test.py
```
Tests semantic text clicking.

---

## Performance Metrics

- **Loop Time**: 3-5 seconds (screenshot + OCR + LLM call)
- **OCR Speed**: 1-2 seconds
- **LLM Response**: 1-2 seconds
- **Total End-to-End**: 5-10 loops to complete simple task

---

## Future Enhancements

### Phase 2: Workflow Learning
- Persistent graph queries
- Workflow success rate tracking
- Suggest actions from similar past states

### Phase 3: Parallel Tasks
- Multiple independent workflows
- Shared memory for common patterns

### Phase 4: Advanced Perception
- Object detection (CV2)
- Visual similarity matching
- PDF/document handling

### Phase 5: Distributed
- Remote execution
- Multi-machine coordination
- Cloud persistence

---

## Troubleshooting

### Agent Stuck in Loop
- Check Chrome focus: `get_active_window()`
- Verify LLM responding: Check API logs
- Check OCR: Run ocr_test.py

### Actions Not Executing
- Validate action: Check validation rules
- Check logs for blocked actions
- Verify parameters

### Memory Growing
- SQLite persists data: Check db file size
- Graph grows with loops: Normal (features learned)
- Implement cleanup if > 10GB

### OCR Accuracy
- Screenshots unclear: Try adjusting gamma
- Tesseract not found: Install at C:\Program Files\Tesseract-OCR
- Low quality text: Increase screenshot resolution

---

## Code Quality

- **Type Hints**: Partial (add more as needed)
- **Documentation**: Comprehensive docstrings
- **Error Handling**: Try/catch around risky operations
- **Logging**: All major actions logged
- **Testing**: Unit + integration tests included

---

## Author Notes

This architecture prioritizes:
1. **Reliability** over features
2. **Observability** through logging
3. **Determinism** via validation
4. **Learning** through memory
5. **Safety** with focus management

The agent is production-ready for desktop automation with proper monitoring and rate limiting.
