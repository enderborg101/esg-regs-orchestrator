from app.orchestrator.router import route_task
from app.schemas.tasks import AgentName, OrchestrationTask, TaskType


def test_regulatory_analysis_routes_to_claude():
    task = OrchestrationTask(
        objective="Analyse packaging EPR applicability",
        task_type=TaskType.REGULATORY_ANALYSIS,
        primary_agent=AgentName.CLAUDE,
    )
    assert route_task(task) == AgentName.CLAUDE


def test_adversarial_review_routes_to_deepseek():
    task = OrchestrationTask(
        objective="Challenge calculation logic",
        task_type=TaskType.ADVERSARIAL_REVIEW,
        primary_agent=AgentName.DEEPSEEK,
    )
    assert route_task(task) == AgentName.DEEPSEEK
