from fastapi import FastAPI

from app.schemas.tasks import OrchestrationTask
from app.orchestrator.router import route_task

app = FastAPI(title="ESG Regs Orchestrator", version="0.1.0")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/v1/tasks/route")
def route(task: OrchestrationTask) -> dict[str, str]:
    """Validate an orchestration task and return the selected primary agent.

    This is intentionally a thin first milestone. Provider calls and Notion/GitHub
    integrations will be added behind this stable task contract.
    """
    return {"agent": route_task(task).value, "task_type": task.task_type.value}
