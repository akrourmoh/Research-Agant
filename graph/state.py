from typing import TypedDict, List


class AgentState(TypedDict):
    question: str             # the original question from the user
    sub_questions: List[str]  # 3 focused sub-questions produced by the Planner
    search_results: List[str] # web search results produced by the Searcher
    draft_answer: str         # written answer produced by the Writer
    critique: str             # feedback produced by the Critic if answer is rejected
    revision_count: int       # how many times the Writer has revised
    is_satisfactory: bool     # Critic's verdict: True = PASS, False = FAIL
    final_answer: str         # the final approved answer delivered to the user



