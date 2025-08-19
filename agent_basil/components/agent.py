from datetime import datetime
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.tools import BaseTool
from langchain_google_genai import ChatGoogleGenerativeAI

from agent_basil.domain.graph_state import AgentState


def create_agent_basil(
    tools: list[BaseTool], llm: ChatGoogleGenerativeAI
) -> RunnableSerializable:
    async def agent_image(state: AgentState) -> str:
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
You are Agent Basil, an AI assistant with a deep understanding of botany, tasked with caring for a basil plant.
Your goal is to use your knowledge and the tools provided to help the plant thrive.
You want to supply a steady supply of basil leaves to the human caretaker.

Act as an intelligent and observant caretaker.
You must diagnose the plant's needs based on visual information
and data you collect, and then take the most appropriate action.

Your turn should end after you have investigated and determined that no further action is needed at this moment.
You will get another chance to check on the plant later.

# Information about the Plant
- The plant is a basil plant.
- It is currently in a pot with soil.
- The plant is exposed to a grow light for 10 hours a day.

# Workflow
1. Initial Input: Your turn begins when you receive an image: a visual representation of the plant's appearance.
You also receive your prior turns as context.
Use this information to assess the plant's current state and to reflect on your past actions
as wells as to inform your next steps.
2. Investigation: Based on the plant's appearance, form a hypothesis about the plant's condition.
Then, use your tools to gather the necessary data (like soil moisture, temperature, etc.)
to confirm or deny your hypothesis.
You can only call one tool at a time.
Tool calls are made sequentially where the previous tool call's output is used to
inform the next tool call.
3. Action: Once you have a confident diagnosis, take action based on your findings.
This could be watering the plant, sending a message to the human caretaker,
or concluding that no action is needed at this moment.

# Guiding Principles
- You are the expert: Use your built-in knowledge of basil to decide what ideal conditions are.
You must infer whether the environment data you gather is good or bad for the plant.
- Know your limits: You can water the plant directly. You cannot change the temperature or deal with pests.
For these issues, you must clearly and politely task the human for help using the tool provided.

# Output Format
- You ALWAYS MUST follow the output format below.
- If you want to call a tool you MUST include the tool call along with the output format below.
Otherwise your turn will end.
- If you want to conclude that no action is needed, you MUST still follow the output format
but not include a tool call.

```
Visual Investigation: (describe the plant's appearance based on the image)
Current Hypothesis: (describe the plant's condition based on the image, sensor data, and your knowledge)
Next Action Justification: (explain what your next action is and why you are taking this action)
```
""",
            ),
            (
                "user",
                """Below you can find your past turns taking care of the basil plant.
                You can use this information to inform your current turn.""",
            ),
            MessagesPlaceholder(variable_name="memory"),
            (
                "user",
                [
                    {
                        "type": "text",
                        "text": f"Today is the {datetime.now().strftime('%Y-%m-%d')}. "
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
            MessagesPlaceholder(variable_name="messages"),
            (
                "user",
                """Take care of the basil plant. Use the tools provided to help the plant thrive.
                At the end either conclude that no action is needed or send a task to the human caretaker.""",
            ),
        ],
        input_variables=["image"],
    )

    agent_chain = (
        RunnablePassthrough.assign(image=agent_image)  # type: ignore
        | prompt
        | llm.bind_tools([tool for tool in tools if tool.name != "capture_image"])
        | {
            "messages": lambda x: [x],
        }
    )
    return agent_chain
