# Extending the Basic JWKS Server

## Objective

This project aims to enhance a JWKS server to protect against SQL injection vulnerabilities by utilizing a SQLite database to store private keys. By integrating a database, we ensure that private keys are persisted to disk, allowing availability even after server restarts. This project emphasizes secure SQL query handling to prevent injection attacks.

## Background

SQLite is a serverless, single-file database. This project modifies the previous implementation to:
- Create/open a SQLite DB file on startup.
- Write private keys to the database.
- Modify the `POST /auth` and `GET /.well-known/jwks.json` endpoints to use the database.

## Requirements

### SQLite Backed Storage

- **Database File Name**: `totally_not_my_privateKeys.db`
- **Table Schema**:
  ```sql
  CREATE TABLE IF NOT EXISTS keys(
      kid INTEGER PRIMARY KEY AUTOINCREMENT,
      key BLOB NOT NULL,
      exp INTEGER NOT NULL
  );
