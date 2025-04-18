# Architecture Guide: PromptSculptor API (Prototype v1)

## 1. Selected Architecture Pattern

*   **Pattern:** Monolithic Backend Application
*   **Description:** A single Python application built using the FastAPI framework will serve all API endpoints. This approach prioritizes simplicity and development speed for the initial prototype.
*   **Justification:** The prototype has a limited, well-defined scope (3 core endpoints, API-only, no user accounts). A monolith provides the simplest structure for development, testing, and initial deployment, directly aligning with the goal of quickly building a functional core.

## 2. State Management

*   **Frontend:** N/A (API Only).
*   **Backend:** Primarily stateless. Each API request (`/analyze`, `/remix`, `/create`) will be processed independently. No server-side session management is required for the prototype. If any data needs persistence beyond a single request (e.g., for potential future logging or rate limiting, though not in v1 scope), it will be handled by the database.

## 3. Technical Stack

*   **Frontend:** N/A
*   **Backend:**
    *   Language/Framework: **Python 3.10+ / FastAPI**
    *   Database: **SQLite** (for simplicity in the prototype)
    *   ORM: **SQLModel** (integrates Pydantic models with SQLAlchemy)
    *   Server: Uvicorn (ASGI server)
*   **Authentication:** None implemented for Prototype v1. Endpoints are public.
*   **Payments:** N/A
*   **Key Integrations:**
    *   **External LLM Service:** Requires integration with at least one Large Language Model provider (e.g., OpenAI API, Anthropic API, Google Gemini API, or a self-hosted model) via their respective Python clients/SDKs. This is essential for the core logic of `/analyze`, `/remix`, and `/create`. API keys and configuration for this service will be managed via environment variables.

## 4. Authentication & Authorization Flow

*   N/A for Prototype v1. All endpoints will be publicly accessible without authentication or authorization checks.

## 5. High-Level Route Design

*   **Frontend:** N/A
*   **Backend API Endpoints:** All endpoints will likely be grouped under a base path (e.g., `/api/v1/`) for future versioning, although not strictly required for the prototype.
    *   `POST /api/v1/analyze`: Handles prompt analysis requests.
    *   `POST /api/v1/remix`: Handles prompt remixing requests.
    *   `POST /api/v1/create`: Handles prompt creation requests.

## 6. API Design Philosophy

*   **Style:** RESTful principles. Use standard HTTP methods (POST for actions).
*   **Data Format:** JSON for request bodies and responses.
*   **Versioning:** No explicit versioning enforced in v1, but use of a `/api/v1/` path prefix is recommended.
*   **Error Handling:** Use standard HTTP status codes (e.g., `200 OK`, `400 Bad Request` for client errors like invalid input, `422 Unprocessable Entity` for validation errors via Pydantic, `500 Internal Server Error` for unexpected server issues, `503 Service Unavailable` if the external LLM is down). FastAPI's built-in exception handling will be used, potentially with custom handlers for specific errors (like external API failures).

## 7. Database Design Overview

*   **Database:** **SQLite**. A single file-based database (`promptsculptor_proto.db`) will be used.
*   **ORM:** **SQLModel**.
*   **Key Models:** The initial prototype endpoints (`/analyze`, `/remix`, `/create`) might not strictly require database persistence *for their core function* if results are generated and returned immediately. However, the Data Architect may define models for potential future use cases like logging requests/responses, storing predefined remix styles, or caching results, even if not fully utilized in v1. The detailed schema will be defined by the Data Architect using SQLModel.

## 8. Deployment & Infrastructure Overview

*   **Target Hosting:** Flexible. Can be run locally for development, containerized using Docker, or deployed to simple PaaS (e.g., Heroku, Fly.io) or a VM.
*   **Deployment:** Manual deployment or simple script using `uvicorn` for the prototype.
*   **CI/CD:** Out of scope for the initial prototype setup. Future implementation could use GitHub Actions or similar tools.
*   **Configuration:** Environment variables (`.env` file) for settings like the external LLM API key.

## 9. Future Architecture Evolution (Post-Prototype)

While the initial prototype utilizes a simple monolithic architecture, future iterations will likely require evolution to handle increased complexity, user management, and scalability demands.

*   **API Gateway Integration (Kong):** As requirements like authentication, rate limiting, and centralized routing emerge, introducing an API Gateway like Kong is highly recommended.
    *   **Role:** Kong would sit in front of the FastAPI application(s), handling incoming client requests.
    *   **Responsibilities:**
        *   **Authentication:** Implement API key validation (`key-auth` plugin) or JWT validation (`jwt` plugin) centrally.
        *   **Rate Limiting:** Apply request limits per consumer (`rate-limiting` plugin).
        *   **Routing:** Manage routing rules, potentially directing traffic to different backend services if the monolith is later broken down.
        *   **Load Balancing:** Distribute traffic across multiple instances of the FastAPI application.
        *   **Security:** TLS termination, IP restrictions.
        *   **Monitoring:** Integrate with monitoring tools (e.g., Prometheus plugin).
    *   **Deployment:** Kong would run as a separate containerized service, configured declaratively or via its Admin API. The FastAPI application would then only need to be accessible by Kong.
*   **Database Migration:** SQLite is suitable for the prototype but will likely become a bottleneck. Migrating to a more robust relational database like **PostgreSQL** or **MySQL** will be necessary to support:
    *   Higher concurrency and write loads.
    *   More complex relational data (user accounts, prompt history, saved configurations).
    *   Advanced querying capabilities.
    *   SQLModel supports these databases, easing the transition.
*   **Potential Service Decomposition:** If the application grows significantly complex, the monolith could be decomposed into smaller, more focused microservices (e.g., a dedicated service for analysis, another for generation, a user management service). Kong would be crucial for routing requests to the appropriate service.
*   **CI/CD Implementation:** Formal CI/CD pipelines (e.g., using GitHub Actions) should be established for automated testing, building container images, and deploying updates to Kong and the backend application(s).
*   **Monitoring & Observability:** Integrate comprehensive monitoring (metrics, logging, tracing) using tools potentially integrated with Kong (Prometheus, Grafana, Datadog) and within the FastAPI application itself.
