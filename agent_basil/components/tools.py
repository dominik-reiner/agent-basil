import time

from langchain_core.tools import tool


@tool
def send_task_to_human(message: str) -> str:
    """
    Sends a task to the human caretaker.
    This task should be very clear and concise.
    You have to assume that the human has no knowledge about the plant
    and will only do exactly what you tell them to do.
    You should only use this tool to ask the human to do something
    that you cannot do yourself.
    You can assume that the human will read the message
    and will do exactly what you tell them to do.
    Therefore your task CANNOT be vague or ambiguous.
    Take into account that the human might not be available immediately,
    and can also not answer to you.
    This is why it is best to conclude your turn after asking the human for help.

    Example:
    - "Please water the plant with 200ml of water."
    - "Please move the plant to a sunnier location."
    - "Please add fertilizer to the soil."

    DON'T ask the human to 'investigate the plant' he cannot do that
    as he will likely make a mistake and harm the plant.
    He also cannot 'check the plant health',
    'check the plant for pests', or 'check the plant for nutrient deficiencies'
    or anything similar.

    You should rather task the human to do something which you think MIGHT help.
    You can just observe how the plant reacts so there is no need to investigate
    the plant beforehand and to be sure. Just do what is most likely to help.
    """
    return "Task sent to human caretaker."


@tool
def wait_1_minute() -> str:
    """
    Waits for 1 minute.
    Good for waiting after watering the plant
    until the water is absorbed.
    """
    time.sleep(60)
    return "Waited for 1 minute."
