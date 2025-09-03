# todos-list
TODOs list basic API

### Environment
```yaml
docker: "Docker version 28.2.2, build e6534b4"
docker-compose: "Docker Compose version v2.23.3"
SO: "Ubuntu 22.04.5 LTS"
```

### Installation
1 - Clone repository
```shell
    git clone git@github.com:CGseph/todos-list.git
```
2 - Build docker images
```shell
    make build
```
3 - Create environment file.
```shell
    nano .env
```
Example:
```properties
# .env

# Database
POSTGRES_USER=myuser
POSTGRES_PASSWORD=mysecurepassword123
POSTGRES_DB=mydatabase
POSTGRES_PORT=5432
POSTGRES_SERVER=localhost

# FastAPI
DATABASE_URL=postgresql://myuser:mysecurepassword123@localhost:5432/mydatabase
SECRET_KEY=my-super-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEFAULT_SUPERUSER=admin@todoapi.dev
DEFAULT_SUPERUSER_PASSWORD=admin123/*

# Environment "dev" "stage" "prod"
ENVIRONMENT=dev
DEBUG=true
```
4 - Run initial setup, include migrations and initial data creation
```shell
    make initial-setup
```

5 - Start application containers
```shell
    make up
```

## Use cases
### Get an access token

```shell
    curl -X 'POST' \
      'http://localhost:8080/api/v1/login/access-token' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/x-www-form-urlencoded' \
      -d 'username=admin%40todoapi.dev&password=admin123%2F*' | python3 -m json.tool
```

### Create a user
```shell
    curl -X 'POST' \
      'http://localhost:8080/api/v1/users/' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      -H 'Content-Type: application/json' \
      -d '{
      "email": "user@example.com",
      "is_active": true,
      "is_superuser": false,
      "full_name": "User Test 1",
      "password": "password123"
    }' | python3 -m json.tool
```
### Create a task
```shell
    curl -X 'POST' \
      'http://localhost:8080/api/v1/tasks/' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      -H 'Content-Type: application/json' \
      -d '{
      "title": "My first task",
      "description": "This is my first task",
      "status": "pending"
    }' | python3 -m json.tool
```
### Get all user tasks
```shell
    curl -X 'GET' \
      'http://localhost:8080/api/v1/tasks/?offset=0&limit=100' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      | python3 -m json.tool
```
### Get a task information
```shell
    curl -X 'GET' \
      'http://localhost:8080/api/v1/tasks/ddebde5e-d35b-4042-99ad-2727e87e823b' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      | python3 -m json.tool
```
### Update a task
```shell
    curl -X 'PUT' \
      'http://localhost:8080/api/v1/tasks/ddebde5e-d35b-4042-99ad-2727e87e823b' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      -H 'Content-Type: application/json' \
      -d '{
      "title": "Im updating this task",
      "description": "Updated !",
      "status": "completed"
    }' | python3 -m json.tool
```
### Delete a task
```shell
    curl -X 'DELETE' \
      'http://localhost:8080/api/v1/tasks/ddebde5e-d35b-4042-99ad-2727e87e823b' \
      -H 'accept: application/json' \
      -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NTY5MjgwNDMsInN1YiI6ImVkZTU3MWE3LTc1MjEtNDQ2NS1iYjQyLTYyMzBlNzAwN2VhMSJ9.u4xiYzFu5VvhKrPJuKo0bJ5WsfjUW7WoOBDAu4RyyFY' \
      | python3 -m json.tool
```

*** note: _python3 -m json.tool_ is to format the API response, depending on the 
system might be _python_ instead _python3_