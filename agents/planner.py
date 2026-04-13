from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from graph.state import AgentState
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3-flash-preview", temperature=0)

def planner_agent(state: AgentState) -> dict:
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are a research planner.
        Your job is to take the user's question and break it down into exactly 3 focused sub-questions.
        These sub-questions together must fully cover the original question.
        Return only a numbered list like this:
        1. first sub-question
        2. second sub-question
        3. third sub-question
        Nothing else."""),
        ("human", "{question}")
    ])

    chain = prompt | llm
    result = chain.invoke({"question": state["question"]})

    content = result.content if isinstance(result.content, str) else result.content[0]["text"]

    lines = [line.strip() for line in content.strip().split("\n") if line.strip()]
    sub_questions = [line.split(". ", 1)[-1] for line in lines if line[0].isdigit()]

    return {"sub_questions": sub_questions}
