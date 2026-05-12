def verify(previous_obs, current_obs):

    previous = previous_obs["text"].strip()
    current = current_obs["text"].strip()

    changed = previous != current

    return {
        "success": changed,
        "previous": previous[:200],
        "current": current[:200]
    }