# 11 — Failure Modes & Mitigations

| Failure Mode | Root Cause | DocuPilot Mitigation |
| :--- | :--- | :--- |
| **Split Context** | Answer spans across two chunks. | Sliding window overlap (`150` chars) and paragraph boundary awareness. |
| **Retrieval Miss** | Query uses different vocabulary from document. | Dense vector embeddings (`FastEmbed` / `bge-small`) capturing semantic similarity. |
| **Hallucination** | LLM invents facts when documents lack data. | Low temperature (`0.1`) + explicit refusal prompt instructions. |
| **Conflicting Docs** | Two documents state contradictory policies. | Source attribution displays file names and pages so user can verify. |
| **Port Conflicts** | Default port `5432` already allocated on host machine. | Mapped host port to `5433` in `docker-compose.yml`. |
