from langchain_google_genai import ChatGoogleGenerativeAI


def get_llm() -> ChatGoogleGenerativeAI:
    """
    Returns the LLM instance for the agent.
    """
    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0.5,
        max_output_tokens=5000,
    )
