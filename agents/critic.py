from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))

def critic_agent(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a strict quality reviewer.
        Evaluate the answer based on these 3 criteria:
        1. Does it fully and completely answer the original question?
        2. Is it well structured and easy to read?
        3. Are all claims supported by the search results?

        You must reply in exactly this format:
        VERDICT: PASS or FAIL
        CRITIQUE: your detailed feedback explaining what is good or what needs improvement"""),
        ("human", """Question: {question}

        Answer to evaluate:
        {draft_answer}""")
    ])

    chain = prompt | llm
    result = chain.invoke({
        "question": state["question"],
        "draft_answer": state["draft_answer"]
    })

    content = result.content if isinstance(result.content, str) else result.content[0]["text"]
    is_pass = "VERDICT: PASS" in content

    if is_pass:
        return {
            "is_satisfactory": True,
            "critique": content,
            "final_answer": state["draft_answer"],
            "revision_count": state.get("revision_count", 0)
        }
    else:
        return {
            "is_satisfactory": False,
            "critique": content,
            "final_answer": "",
            "revision_count": state.get("revision_count", 0) + 1
        }
