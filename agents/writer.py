from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

def writer_agent(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research writer.
        Your job is to write a comprehensive, well-structured answer to the question.
        Use the search results provided as your source of information.
        Structure your answer with clear sections and reference sources where relevant.
        If you received a critique from a previous review, use it to improve your answer."""),
        ("human", """Question: {question}

        Search Results:
        {search_results}

        Previous Critique (if any): {critique}

        Write a comprehensive answer:""")
    ])

    chain = prompt | llm
    result = chain.invoke({
        "question": state["question"],
        "search_results": "\n\n".join(state["search_results"]),
        "critique": state.get("critique", "None")
    })

    content = result.content if isinstance(result.content, str) else result.content[0]["text"]
    return {"draft_answer": content}
