#!/usr/bin/env python3
"""
Desktop Agent Entry Point
Autonomous desktop automation agent with memory graph
"""

import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
from desktop_agent.core.logger import setup_logger

logger = setup_logger(log_file=str(project_root / "agent.log"))

logger.info("=" * 60)
logger.info("DESKTOP AGENT START")
logger.info("=" * 60)

try:
    # Start the main loop
    from desktop_agent.core.loop_agent import run_agent
    run_agent()
    
except KeyboardInterrupt:
    logger.warning("Agent interrupted by user")
    sys.exit(0)
except Exception as e:
    logger.error(f"Fatal error: {e}", exc_info=True)
    sys.exit(1)
finally:
    logger.info("=" * 60)
    logger.info("DESKTOP AGENT SHUTDOWN")
    logger.info("=" * 60)
