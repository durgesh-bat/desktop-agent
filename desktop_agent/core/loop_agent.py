"""
Main agent loop: observe -> plan -> execute -> verify -> retry
Integrates all components with logging and memory graph tracking.
"""

import time
import keyboard

from .observer import observe
from .planner import plan
from .executor import execute_actions
from .verifier import verify
from .state import state
from .validator import validate_action
from .goal_checker import is_task_complete
from .logger import logger, log_section, log_result, log_action

from ..memory.memory_graph import (
    add_memory_node,
    add_memory_edge,
    print_graph
)
from ..memory.workflow_memory import workflow_memory
from ..perception.state_classifier import classify_state


MAX_RETRIES = 5
LOOP_COOLDOWN = 2
ACTION_TIMEOUT = 3


def run_agent(task="Open Chrome and search latest AI news"):
    """
    Run the main agent loop.
    
    Args:
        task: High-level task description
    """
    logger.info(f"Starting agent with task: {task}")
    
    last_state_node = None
    loop_count = 0
    workflow_id = workflow_memory.start_workflow(
        "search_task",
        f"Task: {task}"
    )
    
    try:
        while True:
            loop_count += 1
            logger.info(f"\n--- LOOP {loop_count} ---")
            
            # Emergency stop
            if keyboard.is_pressed("esc"):
                logger.warning("Stopped by user (ESC pressed)")
                break
            
            # =====================
            # OBSERVE
            # =====================
            log_section("OBSERVE")
            before = observe()
            logger.debug(f"Screen text (first 100 chars): {before['text'][:100]}")
            
            # Classify current state
            current_state = classify_state(before)
            logger.info(f"Current state: {current_state}")
            
            # Add to memory graph
            add_memory_node(
                current_state,
                data={"text": before["text"][:200]}  # Store only first 200 chars
            )
            
            if last_state_node:
                add_memory_edge(
                    last_state_node,
                    current_state,
                    action="observe"
                )
            
            workflow_memory.add_state_to_workflow(current_state)
            last_state_node = current_state
            
            # =====================
            # CHECK GOAL
            # =====================
            completed = is_task_complete(task, before)
            if completed:
                log_section("GOAL_CHECK", "COMPLETE ✓")
                workflow_memory.complete_workflow(f"search_task_{loop_count}", success=True)
                print_graph()
                break
            
            # =====================
            # PLAN
            # =====================
            log_section("PLAN")
            action = plan(task, before)
            logger.info(f"Planned action: {action.get('action', 'unknown')}")
            log_action(action.get('action', 'unknown'), str(action).replace('\n', ' ')[:100])
            
            # Add action to memory
            action_node = f"action_{int(time.time() * 1000)}"
            add_memory_node(action_node, data={"action": action.get("action")})
            add_memory_edge(current_state, action_node, action="plan")
            workflow_memory.add_action_to_workflow(action_node)
            
            # =====================
            # VALIDATE
            # =====================
            valid = validate_action(action, before)
            logger.info(f"Action valid: {valid}")
            if not valid:
                logger.warning("Invalid action blocked, skipping")
                continue
            
            # =====================
            # EXECUTE
            # =====================
            log_section("EXECUTE")
            try:
                execute_actions([action], before["image"])
                logger.info("Action executed")
            except Exception as e:
                logger.error(f"Execution error: {e}", exc_info=True)
                continue
            
            time.sleep(ACTION_TIMEOUT)
            
            # =====================
            # VERIFY
            # =====================
            log_section("VERIFY")
            after = observe()
            result = verify(before, after)
            success = result.get("success", False)
            log_result(success, result.get("details", ""))
            logger.info(f"Verification result: {success}")
            
            # Update memory with result
            new_state = classify_state(after)
            add_memory_node(new_state, data={"text": after["text"][:200]})
            add_memory_edge(
                action_node,
                new_state,
                action="execute",
                outcome="success" if success else "failed"
            )
            workflow_memory.add_state_to_workflow(new_state)
            last_state_node = new_state
            
            # =====================
            # RETRY LOGIC
            # =====================
            if success:
                state["retries"] = 0
                state["last_success"] = action
                logger.info("Action succeeded, resetting retry counter")
            else:
                state["retries"] += 1
                logger.warning(f"Action failed. Retry {state['retries']}/{MAX_RETRIES}")
                
                if state["retries"] >= MAX_RETRIES:
                    logger.error("Max retries exceeded, stopping")
                    workflow_memory.complete_workflow(
                        f"search_task_{loop_count}",
                        success=False
                    )
                    print_graph()
                    break
            
            # =====================
            # CHECK DONE
            # =====================
            if action.get("action") == "done":
                logger.info("Agent marked task as done")
                workflow_memory.complete_workflow(
                    f"search_task_{loop_count}",
                    success=True
                )
                print_graph()
                break
            
            # Cooldown between loops
            time.sleep(LOOP_COOLDOWN)
    
    except Exception as e:
        logger.error(f"Unexpected error in loop: {e}", exc_info=True)
        raise
    finally:
        logger.info(f"Agent loop ended after {loop_count} iterations")
        logger.info(f"Final state: {state}")


if __name__ == "__main__":
    run_agent()
