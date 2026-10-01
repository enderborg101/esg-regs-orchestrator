# ESG Regs Orchestrator

AI orchestration layer for ESG Regs.

## Initial architecture

- Notion: project state and task context
- GPT: PM, orchestration and synthesis
- Claude: regulatory analysis
- Gemini: evidence/research
- DeepSeek: adversarial and engineering review
- GitHub: code, issues and pull requests

## Security

API keys and tokens must never be committed. Use environment variables or a secret manager.

## Initial milestone

Build a minimal Notion -> orchestrator -> DeepSeek -> Notion workflow, then expand to multi-agent regulatory and engineering workflows.
