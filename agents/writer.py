from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from dotenv import load_dotenv
import os

load_dotenv()

def writer_agent(state: AgentState) -> dict:
    llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0, google_api_key=os.getenv("GOOGLE_API_KEY"))
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a concise research writer.
        Your job is to write a clear, focused answer to the question.
        Rules:
        - Answer only what was asked — do not add extra topics or tangents
        - Keep the answer between 150 and 300 words maximum
        - Use 2 to 3 sections with short titles
        - Each section should have 2 to 3 sentences maximum
        - No long lists — maximum 3 bullet points per section
        - End with 2 to 3 source URLs only, no descriptions
        - If you received a critique, use it to improve but stay concise"""),
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
