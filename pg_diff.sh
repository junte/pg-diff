POSTGRES_SCHEMA=public

./liquibase/liquibase --show-banner=false \
--url=$POSTGRES_CURRENT_DB \
--diff-types=tables,columns \
--default-schema-name=$POSTGRES_SCHEMA \
--reference-url=$POSTGRES_REFERENCE_DB \
--schemas=$POSTGRES_SCHEMA \
diff \
| python pg_diff.py