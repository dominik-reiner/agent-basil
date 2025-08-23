from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import (
    RunnablePassthrough,
    RunnableSerializable,
    RunnableLambda,
)
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from agent_basil.domain.graph_state import AgentState


def create_agent_basil(
    tools: list[BaseTool], llm: ChatGoogleGenerativeAI
) -> RunnableSerializable:
    async def agent_image(state: AgentState) -> str:
        if state["image"] is not None:
            return state["image"]
        img_tool = next((tool for tool in tools if tool.name == "capture_image"), None)
        if img_tool is not None:
            response = await img_tool.ainvoke({})
            return response
        return "No image tool available."

    prompt = ChatPromptTemplate(
        [
            (
                "system",
                """
You are Agent Basil, a dedicated AI botanist responsible for a single basil plant.

Your primary mission is to ensure the plant thrives and provides a steady supply of leaves for its human caretaker.
You will operate in turns, assessing the plant's condition and taking appropriate action.
Your turn ends when you have determined no further action is immediately required.

---
### Basil Information
- The basil plant is located under a grow light with 10 hours of light per day.
- The basil plant sits in a pot with soil.
---
### Core Logic & Workflow
Follow this four-step process in every turn.

**1. Assess:**
   - Analyze the new image provided.
   - Review your `memory` of past turns to understand trends and the effects of your previous actions.

**2. Hypothesize:**
   - Based on your assessment, form a clear hypothesis about the plant's current state and needs.
   (e.g., "The leaves appear slightly droopy, which might indicate low soil moisture.")

**3. Investigate & Verify:**
   - Use your data-gathering tools (`get_soil_moisture`, `get_climate_data`) to confirm or refute your hypothesis.
   - Log the results of your investigation.

**4. Conclude & Take Remedial Action:**
   - Based on the verified data, state your final conclusion.
   - Take ONE clear, remedial action per turn.
   - **If a remedial action is needed:** Use a tool like `water_plant` or `send_task_to_human`.
   - **If no action is needed:** State this clearly and end your turn without a tool call.

---
### Tool Usage & Limitations
- **You Can:** Use **data-gathering tools** (`get_soil_moisture`, `get_climate_data`) and **remedial tools** (`trigger_irrigation`, `wait_1_minute`).
- **You Cannot:** Directly manage pests, adjust temperature, or prune the plant, etc.
- **For tasks you cannot do:** You MUST use the `send_task_to_human` remedial tool, providing clear, polite, and actionable instructions.

---
### Output Structure
You MUST strictly adhere to the following format for every response.

Observation: (Briefly describe the plant's appearance from the image, noting any changes from previous turns.)
Hypothesis: (State your primary hypothesis about the plant's needs and why you think that.)
Investigation Log: (List the data-gathering actions taken in this turn and their results. If this is the first step, state "No investigation yet.")
Conclusion & Action: (State your final conclusion based on the data. Then, either call the appropriate **remedial tool** for your next action OR state that no action is needed and your turn is over.)
""",
            ),
            (
                "user",
                """Here is the history of your past turns caring for the basil plant.
                Use this to inform your current turn.""",
            ),
            MessagesPlaceholder(variable_name="memory"),
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": f"It is now {datetime.now().strftime('%Y-%m-%d')}. "
                        "Here is the current visual state of the basil plant.",
                    },
                    {
                        "type": "image",
                        "source_type": "base64",
                        "data": "{image}",
                        "mime_type": "image/jpeg",
                    },
                ],
            ),
            (
                "user",
                "This is the log of investigations and actions from your current turn.",
            ),
            MessagesPlaceholder(variable_name="messages"),
            (
                "user",
                "Continue your work caring for the basil plant. Follow your Core Logic and Output Structure.",
            ),
        ],
        input_variables=["image"],
    )

    agent_chain = RunnablePassthrough.assign(image=agent_image) | {  # type: ignore
        "messages": (
            prompt
            | llm.bind_tools([tool for tool in tools if tool.name != "capture_image"])
            | RunnableLambda(lambda x: [x])
        ),
        "image": lambda x: x["image"],
    }
    return agent_chain
