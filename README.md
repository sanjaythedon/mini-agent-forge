# Mini Agent Forge

A full-stack application featuring a WebSocket-based chat interface with backend services for handling real-time communication and data processing.

## Table of Contents
- [Backend](#backend)
  - [Modules](#backend-modules)
  - [Setup with Docker Compose](#backend-docker-compose)
  - [Running Tests](#backend-tests)
- [Frontend](#frontend)
  - [Setup](#frontend-setup)
  - [Running the Application](#running-the-application)

## Backend

The backend is built with FastAPI and provides WebSocket endpoints for real-time communication along with RESTful APIs.

### Backend Modules

1. **API Layer** (`api.py`)
   - Handles HTTP and WebSocket connections
   - Manages CORS and request/response handling
   - Exposes endpoints for chat history and real-time communication

2. **WebSocket Manager** (`ws_manager/`)
   - Manages WebSocket connections
   - Handles message routing and broadcasting
   - Implements connection lifecycle management

3. **Database** (`Database/`)
   - PostgreSQL database for persistent storage
   - Handles data models and database operations

4. **Redis** (`Redis/`)
   - Used for caching and pub/sub functionality
   - Manages real-time message queuing

5. **LLM Integration** (`LLM/`)
   - Integrates with language models
   - Processes and generates responses

6. **Tools** (`Tools/`)
   - Contains utility functions and helpers
   - Implements various tools used by the application

### Setup with Docker Compose

1. Ensure Docker and Docker Compose are installed on your system

2. Navigate to the backend directory:
   ```bash
   cd backend
   ```

3. Create a `.env` file with the required environment variables:
   ```
   POSTGRES_USER=username
   POSTGRES_PASSWORD=password
   POSTGRES_DB=mydb
   REDIS_HOST=redis
   REDIS_PORT=6379
   REDIS_DB=0
   ```

4. Start the services:
   ```bash
   docker-compose up -d
   ```

5. The backend server will be available at `http://localhost:8000`

### Running Tests

To run the backend tests:

1. Ensure all dependencies are installed (preferably in a virtual environment):
   ```bash
   pip install -r requirements.txt
   ```

2. Run the tests:
   ```bash
   python -m unittest test.py
   ```

## Frontend

The frontend is a modern web application built with a JavaScript framework (React/Vue/Angular).

### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

### Running the Application

1. Start the development server:
   ```bash
   npm run dev
   ```

2. The application will be available at `http://localhost:3000` (or another port if 3000 is in use)

## Environment Variables

### Backend
- `POSTGRES_*`: Database connection settings
- `REDIS_*`: Redis connection settings
- `PORT`: Port to run the backend server (default: 8000)

## Development

- **Backend**: The server will automatically reload when you make changes to the code.
- **Frontend**: The development server supports hot-reloading for a better development experience.
