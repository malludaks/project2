# Extended JWKS Server Project

## Project Overview

This project involves extending a JWKS (JSON Web Key Set) server to incorporate security and persistence features using SQLite. The project highlights essential cybersecurity concepts by protecting the server against SQL injection vulnerabilities and ensuring private keys are stored securely. This server is crucial in modern authentication systems as it serves public keys for verifying JSON Web Tokens (JWTs). 

### Objectives

- Securely store private keys in an SQLite database.
- Ensure keys persist across server restarts, making them available for JWT verification at any time.
- Protect SQL interactions from injection attacks.
- Serve a RESTful API capable of providing valid JWTs and public keys through specific endpoints.

---

## Key Features

- **Secure Database Storage**: Private keys are securely stored in an SQLite database to prevent unauthorized access.
- **SQL Injection Protection**: Ensures all SQL interactions are protected against injection attacks by using parameterized queries.
- **JWT Issuance with Expiration Control**: Generates JWTs that can either be valid or expired, depending on the request.
- **Public Key Retrieval in JWKS Format**: Enables external applications to verify JWTs by accessing the server's public keys.

---

## Requirements

### Environment Setup

- **Python**: Ensure Python 3.7 or newer is installed.
- **SQLite**: SQLite should be installed (it's generally included with most Python installations).


pip install -r requirements.txt

### SQLite Backed Storage

- **Database File Name**: `totally_not_my_privateKeys.db`
- **Table Schema**:
  ```sql
  CREATE TABLE IF NOT EXISTS keys(
      kid INTEGER PRIMARY KEY AUTOINCREMENT,
      key BLOB NOT NULL,
      exp INTEGER NOT NULL
  );

### screenshots
## Coverage Report
![project2 test coverage](https://github.com/user-attachments/assets/ca4b58f6-42e6-4799-bd13-9e399288fe8b)

## Gradebot Test
![project 2 gradebot](https://github.com/user-attachments/assets/50241615-0e92-44f3-b2b6-b2a2584b9d9f)
