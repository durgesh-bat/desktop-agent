import networkx as nx
from ..core.logger import logger, log_memory_event


memory_graph = nx.DiGraph()


def add_memory_node(node_name, data=None):
    """Add a semantic state node to the memory graph."""
    memory_graph.add_node(
        node_name,
        data=data
    )
    log_memory_event("node_added", node_name, str(data)[:50] if data else "")


def add_memory_edge(source, target, action=None, outcome=None):
    """Add a transition edge between states."""
    memory_graph.add_edge(
        source,
        target,
        action=action,
        outcome=outcome
    )
    log_memory_event("edge_added", f"{source} -> {target}", f"action={action}, outcome={outcome}")


def print_graph():
    """Print memory graph structure."""
    logger.info("\n===== MEMORY GRAPH SUMMARY =====")
    logger.info(f"Nodes: {memory_graph.number_of_nodes()}")
    logger.info(f"Edges: {memory_graph.number_of_edges()}")
    logger.info("\n--- Transitions ---")
    
    for edge in memory_graph.edges(data=True):
        source, target, data = edge
        action = data.get('action', 'unknown')
        outcome = data.get('outcome', '?')
        logger.info(f"{source} --[{action}]--> {target} (outcome={outcome})")


def get_node_count():
    """Get number of nodes in graph."""
    return memory_graph.number_of_nodes()


def get_edge_count():
    """Get number of edges in graph."""
    return memory_graph.number_of_edges()


def query_similar_paths(source_state, target_state, limit=3):
    """Query paths between similar states."""
    try:
        paths = list(nx.all_simple_paths(memory_graph, source_state, target_state, cutoff=10))
        return paths[:limit]
    except nx.NetworkXNoPath:
        return []