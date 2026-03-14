#!/bin/bash

set -e
set -u

function create_user_and_database() {
    local username=$1
    local password=$2
    local database=$3
    echo "Creating user '$username' and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "postgres" <<-EOSQL
        CREATE USER $username WITH PASSWORD '$password';
        CREATE DATABASE $database;
        GRANT ALL PRIVILEGES ON DATABASE $database TO $username;
EOSQL
    echo "User '$username' and database '$database' created successfully"
}

# # Metadata database
# create_user_and_database "$METADATA_DATABASE_NAME" "$METADATA_DATABASE_USERNAME" "$METADATA_DATABASE_PASSWORD"

# # Celery database
# create_user_and_database "$CELERY_BACKEND_NAME" "$CELERY_BACKEND_USERNAME" "$CELERY_BACKEND_PASSWORD"

# # ELT database
# create_user_and_database "$ELT_DATABASE_NAME" "$ELT_DATABASE_USERNAME" "$ELT_DATABASE_PASSWORD"

# Metadata database (username, password, database)
create_user_and_database "$METADATA_DATABASE_USERNAME" "$METADATA_DATABASE_PASSWORD" "$METADATA_DATABASE_NAME"

# Celery database (username, password, database)
create_user_and_database "$CELERY_BACKEND_USERNAME" "$CELERY_BACKEND_PASSWORD" "$CELERY_BACKEND_NAME"

# ELT database (username, password, database)
create_user_and_database "$ELT_DATABASE_USERNAME" "$ELT_DATABASE_PASSWORD" "$ELT_DATABASE_NAME"

echo "All databases and users created successfully"