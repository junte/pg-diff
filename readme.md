# Postgres DB diff report

## ENV variables

- `POSTGRES_REFERENCE_DB` - most updated DB state (ex: development DB)
- `POSTGRES_CURRENT_DB` - outdated DB state (ex: PROD DB before release)

## Get report

```bash
docker run --rm -it \
-e "POSTGRES_REFERENCE_DB=jdbc:postgresql://localhost:5432/db-name?user=pg_user&password=secret" \
-e "POSTGRES_CURRENT_DB=jdbc:postgresql://localhost:5432/db-name?user=pg_user&password=secret" \
--network=host ghcr.io/junte/pg-diff:latest
```
