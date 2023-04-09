\set scalargis_db_user `echo ${SCALARGIS_DB_USER}`
\set scalargis_db_password `echo \'${SCALARGIS_DB_PASSWORD}\'`
\set scalargis_db `echo ${SCALARGIS_DB}`
CREATE USER :scalargis_db_user login superuser password :scalargis_db_password;
CREATE DATABASE :scalargis_db;
GRANT ALL PRIVILEGES ON DATABASE :scalargis_db TO :scalargis_db_user;
