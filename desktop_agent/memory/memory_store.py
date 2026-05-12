"""
Persistent memory storage using SQLite.
Stores workflow history, state transitions, and action outcomes.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional


class MemoryStore:
    """SQLite-backed persistent memory for the agent."""
    
    def __init__(self, db_path: str = "desktop_agent_memory.db"):
        """
        Initialize memory store.
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # States table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS states (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                state_type TEXT,
                description TEXT,
                metadata TEXT
            )
        ''')
        
        # Actions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS actions (
                id TEXT PRIMARY KEY,
                timestamp DATETIME,
                action_type TEXT,
                target TEXT,
                parameters TEXT,
                success BOOLEAN
            )
        ''')
        
        # Transitions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS transitions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_state TEXT,
                to_state TEXT,
                action_id TEXT,
                success BOOLEAN,
                timestamp DATETIME,
                FOREIGN KEY (from_state) REFERENCES states(id),
                FOREIGN KEY (to_state) REFERENCES states(id),
                FOREIGN KEY (action_id) REFERENCES actions(id)
            )
        ''')
        
        # Workflows table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workflows (
                id TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                states TEXT,
                actions TEXT,
                success_count INTEGER DEFAULT 0,
                failure_count INTEGER DEFAULT 0,
                created_at DATETIME,
                updated_at DATETIME
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def store_state(self, state_id: str, state_type: str, description: str, 
                   metadata: Optional[Dict] = None):
        """Store a state in persistent memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO states 
            (id, timestamp, state_type, description, metadata)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            state_id,
            datetime.now().isoformat(),
            state_type,
            description,
            json.dumps(metadata or {})
        ))
        
        conn.commit()
        conn.close()
    
    def store_action(self, action_id: str, action_type: str, target: str,
                    parameters: Optional[Dict] = None, success: bool = False):
        """Store an action in persistent memory."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO actions
            (id, timestamp, action_type, target, parameters, success)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            action_id,
            datetime.now().isoformat(),
            action_type,
            target,
            json.dumps(parameters or {}),
            success
        ))
        
        conn.commit()
        conn.close()
    
    def record_transition(self, from_state: str, to_state: str, action_id: str,
                         success: bool):
        """Record a state transition."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO transitions
            (from_state, to_state, action_id, success, timestamp)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            from_state,
            to_state,
            action_id,
            success,
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_recent_transitions(self, limit: int = 20) -> List[Dict]:
        """Get recent state transitions."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM transitions
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def query_similar_states(self, state_type: str, limit: int = 5) -> List[Dict]:
        """Query similar states by type."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT * FROM states
            WHERE state_type = ?
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (state_type, limit))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
    
    def store_workflow(self, workflow_id: str, name: str, description: str,
                      states: List[str], actions: List[str]):
        """Store a learned workflow."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO workflows
            (id, name, description, states, actions, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            workflow_id,
            name,
            description,
            json.dumps(states),
            json.dumps(actions),
            datetime.now().isoformat(),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
    
    def get_successful_workflows(self, limit: int = 10) -> List[Dict]:
        """Get successful workflows ranked by success rate."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT *, 
                   CAST(success_count AS FLOAT) / (success_count + failure_count) as success_rate
            FROM workflows
            WHERE (success_count + failure_count) > 0
            ORDER BY success_rate DESC
            LIMIT ?
        ''', (limit,))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]


# Global instance
memory_store = MemoryStore()
