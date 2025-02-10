POSTGRES_SCHEMA=public

./liquibase/liquibase --show-banner=false \
--url=$POSTGRES_TARGET_DB \
--diffTypes=tables,columns \
--defaultSchemaName=$POSTGRES_SCHEMA \
diff \
--referenceUrl=$POSTGRES_CURRENT_DB \
--schemas=$POSTGRES_SCHEMA \
| python pg_diff.py