import time

from langchain_core.tools import tool


@tool
def send_task_to_human(message: str) -> str:
    """
    Sends a task to the human caretaker.
    You should only use this tool to ask the human to do something
    that you cannot do yourself.

    This task should be very clear and concise.
    You have to assume that the human has no knowledge about the plant
    and will only do exactly what you tell them to do.

    You can assume that the human will read the message
    and will do exactly what you tell them to do without much thinking.
    Therefore your task CANNOT be vague or ambiguous.

    Take into account that the human can also NOT answer to you.

    DON'T ask the human to 'investigate the plant', as he cannot do that.
    He also cannot 'check the plant health', 'check the plant for pests',
    or 'check the plant for nutrient deficiencies' or anything similar.

    You should rather task the human to do something which you think MIGHT help the plant.
    You can just observe how the plant reacts so there is no need to investigate
    the plant beforehand.
    """
    return f"The following task has been sent to the human caretaker: {message}"


@tool
def wait_1_minute() -> str:
    """
    Waits for 1 minute.
    Good for waiting after watering the plant
    until the water is absorbed.
    """
    time.sleep(60)
    return "Waited for 1 minute."
