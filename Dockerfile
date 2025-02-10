FROM python:3.12.9-slim

WORKDIR /app

# Download liquibase package and extract to WORKDIR
RUN apt-get update  \
  && apt-get install -y --no-install-recommends \
  curl=7.* \
  unzip=6.* \
  openjdk-17-jre-headless \
  && curl -o liquibase.zip -SL https://github.com/liquibase/liquibase/releases/download/v4.31.0/liquibase-4.31.0.zip \
  && unzip liquibase.zip -d liquibase \
  && rm liquibase.zip
    
COPY pg_diff.sh .
COPY pg_diff.py .

RUN ["chmod", "+x", "pg_diff.sh"]

CMD "./pg_diff.sh"