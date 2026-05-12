"""
Goal checking: determine if task is complete based on screen state.
Uses keyword matching and semantic understanding.
"""

from .logger import logger


def is_task_complete(task, observation):
    """
    Check if task is complete based on current observation.
    
    Args:
        task: Task description string
        observation: Current screen observation dict
        
    Returns:
        True if task appears complete, False otherwise
    """
    
    text = observation["text"].lower()
    task_lower = task.lower()
    
    logger.debug(f"Checking task completion for: {task}")
    logger.debug(f"Screen text length: {len(text)} chars")
    
    # =====================
    # Search AI News Task
    # =====================
    if "latest ai news" in task_lower or "ai news" in task_lower:

        keywords = [
            "ai news",
            "search results",
            "techcrunch",
            "result",
            "articles",
            "news article"
        ]

        matches = 0
        found_keywords = []

        for keyword in keywords:

            if keyword in text:
                matches += 1
                found_keywords.append(keyword)

        if matches >= 2:
            logger.info(f"Task complete: found {matches} keywords: {found_keywords}")
            return True
        
        logger.debug(f"Task not complete: found {matches}/2 keywords")
        return False
    
    
    # =====================
    # Chrome Open Task
    # =====================
    if "open chrome" in task_lower:
        
        chrome_indicators = ["chrome", "address bar", "google"]
        
        for indicator in chrome_indicators:
            if indicator in text:
                logger.info(f"Task complete: Chrome opened (found '{indicator}')")
                return True
        
        logger.debug("Task not complete: Chrome not yet opened")
        return False
    
    
    # =====================
    # Search Task
    # =====================
    if "search" in task_lower:
        
        search_indicators = [
            "search results",
            "result",
            "results",
            "found",
            "showing"
        ]
        
        for indicator in search_indicators:
            if indicator in text:
                logger.info(f"Task complete: Search completed (found '{indicator}')")
                return True
        
        logger.debug("Task not complete: Search not completed")
        return False
    
    
    # =====================
    # Default: Not Complete
    # =====================
    logger.debug(f"Task type not recognized: {task}")
    return False
