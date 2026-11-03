# SoulSync API

## API Testing Using curl

### 1. Create User (POST)

**Endpoint:** POST /users

**Request body (request.json):**

```json
{
  "name": "Test User",
  "email": "test@example.com"
}
```

**curl command:**

```powershell
curl.exe -i -X POST "http://127.0.0.1:8000/users" -H "Content-Type: application/json" --data-binary "@request.json"
```

**Actual Status Code:** 201 Created

**Result:** User created successfully in PostgreSQL.



### 2. Get User by ID (GET)

**Endpoint:** GET /users/{user_id}

**curl command:**

```powershell
curl.exe -i "http://127.0.0.1:8000/users/5"
```

**Actual Status Code:** 200 OK

**Result:** Retrieved the user using their ID.

**PATCH Verification**

Command:
```powershell
curl.exe -i "http://127.0.0.1:8000/users/5"
```

**Actual Status:** 200 OK

**Result:** The response returned `"name": "Updated User"`, confirming that the updated name was saved and retrieved successfully.


### 2. Get Mood by ID — GET /moods/{mood_id}

**Endpoint:** `GET /moods/3`

**curl Command:**

```powershell
curl.exe -i "http://127.0.0.1:8000/moods/3"
```

**Expected Status:** 200 OK

**Actual Status:** Fill in after executing the command.

**Result:** Verify that mood ID 3 is returned with its stored values.







### Delete Mood — DELETE /moods/{mood_id}

**Endpoint:** `DELETE /moods/3`

**curl Command:**

```powershell
curl.exe -i -X DELETE "http://127.0.0.1:8000/moods/3"
```

**Actual Status:** 204 No Content

**Result:** The API successfully processed the deletion of mood entry ID 3.

**Verification Command:**

```powershell
curl.exe -i "http://127.0.0.1:8000/moods/3"
```

**Expected Verification Status:** 404 Not Found


### Delete Journal — DELETE /journals/{journal_id}

**Endpoint:** `DELETE /journals/1`

**curl Command:**

```powershell
curl.exe -i -X DELETE "http://127.0.0.1:8000/journals/1"
```

**Actual Status:** 204 No Content

**Result:** Journal deletion request completed successfully.

**Verification Command:**

```powershell
curl.exe -i "http://127.0.0.1:8000/journals/1"
```

**Expected Verification Status:** 404 Not Found

### Journal Pagination Validation Test

**Endpoint:** `GET /journals?skip=-1&limit=5`

**curl Command:**

```powershell
curl.exe -i "http://127.0.0.1:8000/journals?skip=-1&limit=5"
```

**Actual Status:** 422 Unprocessable Content

**Result:** The API correctly rejected the negative `skip` value because pagination requires `skip >= 0`.


## Running Locally with Docker

### Requirements
- Docker Desktop
- Docker Compose
- Git

### Setup

1. Clone the repository:

```bash
git clone https://github.com/tiwariji2007/day-2.git
cd day-2
```

2. Create your local environment file:

```powershell
Copy-Item .env.example .env
```

3. Open `.env` and set your own PostgreSQL password. Do not commit this file to GitHub.

4. Start FastAPI and PostgreSQL:

```bash
docker compose up --build
```

5. Open the API documentation:

http://localhost:8000/docs

The default local API port is 8000. If you set `API_PORT=8001`, use port 8001 instead.

### Stop the Application

```bash
docker compose down
```

PostgreSQL data is stored in a Docker named volume and survives normal container restarts.

## Live Deployment

**Platform:** Eigon

**Environment:** dev

**Live API:** https://soulsync-api-5189-app.eigon.app

**Health Check:** https://soulsync-api-5189-app.eigon.app/health

**API Documentation:** https://soulsync-api-5189-app.eigon.app/docs

## Setup Feedback

- Docker Compose needed careful configuration of PostgreSQL environment variables.
- Special characters in the PostgreSQL password caused URL-parsing issues. This was addressed using SQLAlchemy's `URL.create()`.
- Eigon's GitHub integration did not clearly explain the scope of repository access.
- Creating an additional Dev environment initially failed because of environment limitations on the free plan.
