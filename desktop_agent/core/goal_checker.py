def is_task_complete(task, observation):

    text = observation["text"].lower()


    # Example completion logic
    if "latest ai news" in task.lower():

        keywords = [
            "ai news",
            "search results",
            "techcrunch"
        ]

        matches = 0

        for word in keywords:

            if word in text:

                matches += 1

        return matches >= 2


    return False