def classify_state(observation):

    text = observation["text"].lower()


    if "who's using chrome" in text:

        return "chrome_profile_page"


    if "google" in text and "search" in text:

        return "google_search_results"


    if "chatgpt" in text:

        return "chatgpt_home"


    return "unknown_state"