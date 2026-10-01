from app.schemas.tasks import AgentName, OrchestrationTask, TaskType


DEFAULT_ROUTES: dict[TaskType, AgentName] = {
    TaskType.REGULATORY_RESEARCH: AgentName.GEMINI,
    TaskType.REGULATORY_ANALYSIS: AgentName.CLAUDE,
    TaskType.ADVERSARIAL_REVIEW: AgentName.DEEPSEEK,
    TaskType.CODE_REVIEW: AgentName.DEEPSEEK,
    TaskType.SYNTHESIS: AgentName.GPT,
}


def route_task(task: OrchestrationTask) -> AgentName:
    """Return the primary agent, falling back to the standard route for the task type."""
    return task.primary_agent or DEFAULT_ROUTES[task.task_type]
