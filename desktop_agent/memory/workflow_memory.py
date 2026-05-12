"""
Workflow memory management.
Tracks workflows, recognizes patterns, and learns from successful sequences.
"""

from typing import List, Dict, Optional
from datetime import datetime
from .memory_store import memory_store


class WorkflowMemory:
    """Manages learned workflows and their success metrics."""
    
    def __init__(self):
        """Initialize workflow memory."""
        self.current_workflow_id = None
        self.current_workflow_states = []
        self.current_workflow_actions = []
    
    def start_workflow(self, workflow_name: str, description: str = ""):
        """Start tracking a new workflow."""
        self.current_workflow_id = f"workflow_{datetime.now().timestamp()}"
        self.current_workflow_states = []
        self.current_workflow_actions = []
        
        return self.current_workflow_id
    
    def add_state_to_workflow(self, state_id: str):
        """Add a state to current workflow."""
        if state_id not in self.current_workflow_states:
            self.current_workflow_states.append(state_id)
    
    def add_action_to_workflow(self, action_id: str):
        """Add an action to current workflow."""
        if action_id not in self.current_workflow_actions:
            self.current_workflow_actions.append(action_id)
    
    def complete_workflow(self, workflow_name: str, success: bool = True):
        """Mark current workflow as complete."""
        if not self.current_workflow_id:
            return
        
        # Store workflow to persistent memory
        memory_store.store_workflow(
            self.current_workflow_id,
            workflow_name,
            f"Workflow completed at {datetime.now()}",
            self.current_workflow_states,
            self.current_workflow_actions
        )
        
        # Reset
        self.current_workflow_id = None
        self.current_workflow_states = []
        self.current_workflow_actions = []
    
    def get_similar_successful_workflows(self, current_states: List[str], 
                                        limit: int = 3) -> List[Dict]:
        """
        Find successful workflows that match current state sequence.
        
        Args:
            current_states: Current sequence of states
            limit: Number of workflows to return
            
        Returns:
            List of matching workflows
        """
        workflows = memory_store.get_successful_workflows(limit=limit)
        
        # Score workflows by overlap with current states
        scored = []
        for wf in workflows:
            wf_states = wf.get('states', [])
            if isinstance(wf_states, str):
                try:
                    import json
                    wf_states = json.loads(wf_states)
                except:
                    wf_states = []
            
            overlap = len(set(current_states) & set(wf_states))
            if overlap > 0:
                scored.append((wf, overlap))
        
        # Return top matches
        scored.sort(key=lambda x: x[1], reverse=True)
        return [wf for wf, _ in scored[:limit]]
    
    def suggest_next_action(self, current_state: str) -> Optional[Dict]:
        """
        Suggest next action based on workflow history.
        
        Args:
            current_state: Current state ID
            
        Returns:
            Suggested action or None
        """
        # Get recent transitions to understand patterns
        transitions = memory_store.get_recent_transitions(limit=50)
        
        # Find transitions that start from similar states
        candidates = [t for t in transitions if t['from_state'] == current_state]
        
        if not candidates:
            return None
        
        # Return most recent successful transition
        successful = [t for t in candidates if t['success']]
        if successful:
            return successful[0]
        
        return candidates[0] if candidates else None


# Global instance
workflow_memory = WorkflowMemory()
