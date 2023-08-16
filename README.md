# FastAPI Todo App with Pydantic, PostgreSQL, and JWT Authentication

This repository contains a simple Todo application built using FastAPI, Pydantic for data validation, SQLAlchemy for database operations, and JWT for authentication. The app allows users to create, retrieve, update, and delete todo items after authenticating using JSON Web Tokens (JWT). It utilizes a PostgreSQL database for persistent storage.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Authentication](#authentication)
- [Contributing](#contributing)
- [License](#license)

## Features

- User authentication using JWT.
- Create, retrieve, update, and delete todo items.
- Data validation using Pydantic models.
- Persistent storage using PostgreSQL database.
- RESTful API endpoints with FastAPI.
- Clear and structured project organization.

## Prerequisites

Make sure you have the following tools and technologies installed:

- Python (>=3.6)
- PostgreSQL database server
- `pip` package manager

## Installation

1. Clone the repository:

```
git clone https://github.com/boaloysius/fastapi-todo-app.git
cd fastapi-todo-app
```

2. Create a virtual environment (recommended):
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the required packages:
```
pip install -r requirements.txt
```

5. Set up the PostgreSQL database:
- Create a new database named fastapi_todo_db.
- Update the database connection URL in app/config.py.

5. Apply database migrations
```
alembic upgrade head
```

## API Endpoints

Run the FastAPI development server:
```
uvicorn app.main:app --reload
```

The API will be available at http://127.0.0.1:8000.

## API Endpoints
- **GET /todos**: Get a list of all todo items.
- **GET /todos/{todo_id}**: Get details of a specific todo item.
- **POST /todos**: Create a new todo item.
- **PUT /todos/{todo_id}**: Update a todo item.
- **DELETE /todos/{todo_id}**: Delete a todo item.

## Authentication
To use the API endpoints, you need to authenticate by obtaining a JWT token:
1. Send a POST request to /auth/login with the following JSON body:
```
{
  "username": "your_username",
  "password": "your_password"
}
```

2. Receive a JSON response containing the JWT token.
3. Include the JWT token in the Authorization header for subsequent requests:
```
Authorization: Bearer your_jwt_token
```

## Contributing
Contributions are welcome! If you find any bugs or want to add new features, please create an issue or submit a pull request.

## License
This project is licensed under the MIT License


