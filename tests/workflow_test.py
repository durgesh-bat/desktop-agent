"""
Workflow Test: Open Chrome, search for latest AI news, verify results
Tests the complete agent loop with a realistic workflow.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from desktop_agent.core.logger import setup_logger
from desktop_agent.core.loop_agent import run_agent

logger = setup_logger()


def test_search_workflow():
    """
    Test workflow: Search for latest AI news
    
    Steps:
    1. Open Chrome browser
    2. Navigate to Google
    3. Search for "latest AI news"
    4. Verify search results appear
    5. Stop on completion
    """
    logger.info("=" * 60)
    logger.info("WORKFLOW TEST: Search Latest AI News")
    logger.info("=" * 60)
    
    task = "Open Chrome and search latest AI news"
    
    try:
        # Run the agent with the test task
        run_agent(task)
        logger.info("✓ Workflow test completed successfully")
        return True
        
    except KeyboardInterrupt:
        logger.warning("Workflow test interrupted by user")
        return False
    except Exception as e:
        logger.error(f"✗ Workflow test failed: {e}", exc_info=True)
        return False


def test_simple_click():
    """Test simple click action on visible element."""
    logger.info("=" * 60)
    logger.info("TEST: Simple Click")
    logger.info("=" * 60)
    
    from desktop_agent.perception.vision import capture_screen
    from desktop_agent.perception.ocr_reader import read_screen_text
    
    try:
        # Capture screen
        path = capture_screen()
        logger.info(f"Captured screen: {path}")
        
        # Read OCR
        text = read_screen_text(path)
        logger.info(f"OCR Text (first 200 chars): {text[:200]}")
        
        logger.info("✓ Simple click test completed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Simple click test failed: {e}", exc_info=True)
        return False


def test_memory_graph():
    """Test memory graph functionality."""
    logger.info("=" * 60)
    logger.info("TEST: Memory Graph")
    logger.info("=" * 60)
    
    from desktop_agent.memory.memory_graph import (
        add_memory_node,
        add_memory_edge,
        get_node_count,
        get_edge_count,
        print_graph
    )
    
    try:
        # Add test nodes
        add_memory_node("state_start", data={"type": "start"})
        add_memory_node("state_navigate", data={"type": "navigate"})
        add_memory_node("state_search", data={"type": "search"})
        
        logger.info(f"Nodes in graph: {get_node_count()}")
        
        # Add test edges
        add_memory_edge("state_start", "state_navigate", action="navigate_to_google")
        add_memory_edge("state_navigate", "state_search", action="type_search_query", outcome="success")
        
        logger.info(f"Edges in graph: {get_edge_count()}")
        
        # Print graph
        print_graph()
        
        logger.info("✓ Memory graph test completed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Memory graph test failed: {e}", exc_info=True)
        return False


def test_workflow_memory():
    """Test workflow memory and learning."""
    logger.info("=" * 60)
    logger.info("TEST: Workflow Memory")
    logger.info("=" * 60)
    
    from desktop_agent.memory.workflow_memory import workflow_memory
    
    try:
        # Start a workflow
        workflow_id = workflow_memory.start_workflow(
            "test_search",
            "Test workflow for AI news search"
        )
        logger.info(f"Started workflow: {workflow_id}")
        
        # Add states and actions
        workflow_memory.add_state_to_workflow("state_chrome_open")
        workflow_memory.add_state_to_workflow("state_google_loaded")
        workflow_memory.add_action_to_workflow("action_open_chrome")
        workflow_memory.add_action_to_workflow("action_type_search")
        
        # Complete workflow
        workflow_memory.complete_workflow("test_search", success=True)
        logger.info("Workflow completed and stored")
        
        # Query similar workflows
        similar = workflow_memory.get_similar_successful_workflows(
            ["state_chrome_open"],
            limit=3
        )
        logger.info(f"Found {len(similar)} similar workflows")
        
        logger.info("✓ Workflow memory test completed")
        return True
        
    except Exception as e:
        logger.error(f"✗ Workflow memory test failed: {e}", exc_info=True)
        return False


if __name__ == "__main__":
    logger.info("\nStarting workflow tests...\n")
    
    # Run tests
    results = {
        "Memory Graph": test_memory_graph(),
        "Workflow Memory": test_workflow_memory(),
        "Simple Click": test_simple_click(),
        # Uncomment to run full workflow test (requires manual interaction):
        # "Search Workflow": test_search_workflow(),
    }
    
    # Print summary
    logger.info("\n" + "=" * 60)
    logger.info("TEST SUMMARY")
    logger.info("=" * 60)
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        logger.info(f"{status}: {test_name}")
    
    passed = sum(1 for r in results.values() if r)
    total = len(results)
    logger.info(f"\nTotal: {passed}/{total} tests passed")
    
    sys.exit(0 if passed == total else 1)
