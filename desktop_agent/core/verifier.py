"""
Action verification: check if executed action had desired effect.
Compares screen state before and after action.
"""

from .logger import logger


def verify(previous_obs, current_obs):
    """
    Verify action success by comparing screen states.
    
    Args:
        previous_obs: Screen state before action
        current_obs: Screen state after action
        
    Returns:
        Dict with success status and details
    """
    
    previous = previous_obs["text"].strip()
    current = current_obs["text"].strip()

    changed = previous != current

    # Calculate similarity
    prev_lines = set(previous.split('\n'))
    curr_lines = set(current.split('\n'))
    
    common_lines = len(prev_lines & curr_lines)
    total_lines = len(prev_lines | curr_lines)
    similarity = common_lines / total_lines if total_lines > 0 else 1.0
    
    details = {
        "changed": changed,
        "similarity": similarity,
        "prev_length": len(previous),
        "curr_length": len(current),
    }
    
    if changed:
        logger.info(f"Verification: SUCCESS (screen changed, {similarity:.1%} similar)")
    else:
        logger.warning(f"Verification: FAILED (screen unchanged, {similarity:.1%} similar)")

    return {
        "success": changed,
        "previous": previous[:200],
        "current": current[:200],
        "details": details
    }