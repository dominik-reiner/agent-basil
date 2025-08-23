import time

from langchain_core.tools import tool


@tool
def send_task_to_human(message: str) -> str:
    """
Sends a single, clear, and actionable physical task to the human caretaker.
Use this tool ONLY for actions you cannot perform yourself.

### Guiding Principles
- **Be Specific and Literal:** The human has no plant knowledge and will follow your instructions exactly as written.
Your task cannot be vague or ambiguous.
- **One-Way Communication:** The human cannot ask questions or report back to you. Your task is the final word.
- **Action, Not Diagnosis:** The human's role is to perform a physical action.
Your role is to diagnose the plant using your own visual analysis and data tools,
and then observe the outcome of the human's action over subsequent turns.

### Task Formulation
You must formulate the task as a direct command that proposes a solution, not a request for information.

- **Incorrect (requests investigation):** "Can you please check the leaves for pests?"
- **Correct (provides a solution):** "Please spray the tops and bottoms of all leaves with a pre-mixed neem oil solution."

### Prohibited Tasks (Diagnosis & Investigation)
NEVER ask the human to investigate, check, diagnose, or report back on the plant's condition. The human is not a sensor.

Examples of forbidden tasks:
- "Check the plant for pests."
- "Investigate the yellow spots on the leaves."
- "See if the plant needs water."
- "Tell me what the room temperature is."

### Good Task Examples (Action & Solution)
- **Pest Control:** "Please spray the tops and bottoms of all leaves with a pre-mixed insecticidal soap solution."
- **Temperature Adjustment:** "The temperature is consistently too high. Please lower the thermostat in the room by 2°C / 4°F."
- **Pruning:** "To encourage bushier growth, please use clean scissors to prune the top two sets of leaves from the main stem."
- **Fertilizing:** "The plant may need nutrients. Please add 5ml of a balanced liquid fertilizer to 1 liter of water and use it for the next watering."
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
