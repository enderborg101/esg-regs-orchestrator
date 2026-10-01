from enum import Enum
from pydantic import BaseModel, Field


class AgentName(str, Enum):
    GPT = "gpt"
    CLAUDE = "claude"
    GEMINI = "gemini"
    DEEPSEEK = "deepseek"


class TaskType(str, Enum):
    REGULATORY_RESEARCH = "regulatory_research"
    REGULATORY_ANALYSIS = "regulatory_analysis"
    ADVERSARIAL_REVIEW = "adversarial_review"
    CODE_REVIEW = "code_review"
    SYNTHESIS = "synthesis"


class OrchestrationTask(BaseModel):
    objective: str = Field(min_length=1)
    task_type: TaskType
    context: str = ""
    expected_output: str = ""
    primary_agent: AgentName
    reviewers: list[AgentName] = Field(default_factory=list)
    requires_human_review: bool = False
