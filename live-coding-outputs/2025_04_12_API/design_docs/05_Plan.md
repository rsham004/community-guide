# Implementation Plan: PromptSculptor API (Prototype v1)

This plan outlines the development tasks required to build the initial prototype of the PromptSculptor API, based on the finalized design documents.

## Phase 1: Project Setup and Core Backend Foundation

- [ ] Initialize Git repository and project structure according to Architecture Guide (Easy)
- [X] Set up `pyproject.toml` (or `requirements.txt`) with core dependencies (FastAPI, Uvicorn, SQLModel, Pydantic, python-dotenv, httpx, aiosqlite) (Easy)
- [X] Configure basic environment variables (`.env`) for development (e.g., LLM API Key placeholder, DB path) using Pydantic Settings (`app/core/config.py`) (Easy)
- [X] Implement SQLModel `ApiLog` model (`app/models/log.py`) based on Database Design (Easy)
- [X] Set up asynchronous SQLite database connection and session management (`app/db/session.py`) using SQLModel and `aiosqlite` (Medium)
- [X] Implement basic FastAPI application instance (`app/main.py`) with lifespan events for DB connection (optional but good practice) (Medium)
- [X] Create basic Pydantic schemas for API requests/responses (`app/schemas/prompt.py`) based on API Design Spec (Analyze, Remix, Create, ErrorDetail) (Medium)

## Phase 2: Core Service Implementation

- [X] Implement LLM Service (`app/services/llm_service.py`) to handle interaction with the chosen external LLM provider (Medium)
    - [X] Include async HTTP calls using `httpx`.
    - [X] Add basic configuration loading for API keys from `app/core/config.py`.
    - [X] Define placeholder logic for `analyze`, `remix`, and `create` functionalities interacting with the LLM.
- [X] Implement Logging Service (`app/services/logging_service.py`) (Medium)
    - [X] Include function to create and save `ApiLog` entries using the async DB session.
    - [X] Handle serialization of request/response bodies to JSON strings.
- [X] Implement reusable dependencies (`app/core/dependencies.py`) for injecting DB sessions and LLM service clients into API endpoints (Easy)

## Phase 3: API Endpoint Implementation

- [X] Set up API routing (`app/api/router.py`, `app/api/endpoints/prompts.py`) using `APIRouter` (Easy)
- [X] Implement `POST /api/v1/analyze` endpoint (Medium)
    - [X] Inject dependencies (LLM service, DB session).
    - [X] Call `llm_service.analyze`.
    - [X] Call `logging_service.log_request` (potentially via middleware or dependency).
    - [X] Handle request/response using Pydantic schemas.
- [X] Implement `POST /api/v1/remix` endpoint (Medium)
    - [X] Inject dependencies.
    - [X] Call `llm_service.remix`.
    - [X] Call `logging_service.log_request`.
    - [X] Handle request/response using Pydantic schemas.
- [X] Implement `POST /api/v1/create` endpoint (Medium)
    - [X] Inject dependencies.
    - [X] Call `llm_service.create`.
    - [X] Call `logging_service.log_request`.
    - [X] Handle request/response using Pydantic schemas.

## Phase 4: Error Handling, Documentation & Testing

- [X] Implement custom exception classes (e.g., `LLMServiceError`) in `app/services/llm_service.py` (Easy)
- [X] Implement FastAPI exception handlers in `app/main.py` for custom exceptions and potentially generic 500 errors (Medium)
    - [X] Ensure handlers return appropriate `ErrorDetail` responses and status codes (500, 503).
    - [X] Integrate logging of errors via `logging_service`.
- [X] Add basic health check endpoint (`/health`) (Easy)
- [X] Configure and verify auto-generated OpenAPI/Swagger documentation (`/docs`, `/redoc`) (Easy)
- [X] Add basic unit tests for core services (LLM service mock, logging service) (Medium)
- [X] Add basic integration tests for API endpoints (using FastAPI's `TestClient`) (Medium)
- [X] Write `README.md` with setup and run instructions (Easy)

## Future Phases (Post-Prototype v1)

This section outlines potential subsequent phases based on the Architecture Guide and API Design Specification's future enhancements. Task details would be refined before starting each phase.

### Phase 6: Core Prompt Management Implementation (v1.1 Features)

*   **Goal:** Implement initial features for saving, retrieving, and tagging prompts using the existing SQLite database.
*   **Prerequisites:** None (builds on v1 foundation without requiring infrastructure changes).
*   **Tasks:**
    *   [X] Implement SQLModel schemas for simple `Prompt` and `Tag` models in `app/models/prompt_mgmt.py` compatible with SQLite: (Medium)
        *   [X] Basic `Prompt` model with title, description, full_prompt, created_at. (Easy)
        *   [X] Simple `Tag` model with name field. (Easy)
        *   [X] Many-to-many relationship table for prompt-tag associations. (Medium)
    *   [X] Update database session/engine to create new tables. (Easy)
    *   [X] Implement Pydantic schemas for request/response in `app/schemas/prompt_mgmt.py`. (Medium)
    *   [X] **Implement basic API endpoints (`app/api/endpoints/prompt_mgmt.py`):** (Broken down from Hard)
        *   [X] Define router and basic structure. (Easy)
        *   [X] Implement `POST /prompts/` endpoint for creating new prompts with title and content. (Medium)
        *   [X] Implement `GET /prompts/`: List prompts with simple filtering and pagination. (Medium)
        *   [X] Implement `GET /prompts/{id}`: Retrieve specific prompt. (Easy)
        *   [X] Implement `PUT /prompts/{id}`: Update prompt metadata (title, description, tags). (Medium)
        *   [X] Implement `DELETE /prompts/{id}`: Delete prompt. (Easy)
    *   [X] **Add business logic in `app/services/prompt_mgmt_service.py` for prompt management:** (Broken down from Hard)
        *   [X] Implement tag creation and association service. (Medium)
        *   [X] Create prompt retrieval service with tag associations. (Medium)
    *   [X] **Write unit and integration tests:** (Broken down from Hard)
        *   [X] Write unit tests for prompt models and schemas. (Medium)
        *   [X] Write unit tests for tag management. (Medium)
        *   [X] Write integration tests for prompt CRUD operations. (Medium)

### Phase 7: Basic Search Implementation (v1.1 Features)

*   **Goal:** Add capabilities for finding saved prompts using simple search techniques.
*   **Prerequisites:** Phase 6.
*   **Tasks:**
    *   [X] **Basic Search:**
        *   [X] Implement `POST /prompts/search` endpoint for keyword/tag-based search. (Medium)
        *   [X] Add service logic for filtering based on query parameters/body. (Medium)
    *   [X] Write tests for search functionality. (Medium)

### Phase 8: Feature Expansion (v1.1+ Features)

*   **Goal:** Implement additional endpoints from the PRD.
*   **Prerequisites:** Phase 6.
*   **Tasks:**
    *   [ ] **Implement additional endpoints:** (Broken down from Hard)
        *   [ ] Design and implement `POST /api/v1/test` endpoint for multi-LLM testing. (Medium)
        *   [ ] Design and implement `POST /api/v1/contextualize` endpoint for adapting prompts to personas. (Medium)
        *   [ ] Design and implement `POST /api/v1/combine` endpoint for merging prompt fragments. (Medium)
    *   [ ] Add support for additional LLM providers in `LLMService`. (Medium)

### Phase 5: Infrastructure & Deployment Upgrade (v1.2 Features)

*   **Goal:** Upgrade infrastructure to support advanced features and scaling.
*   **Prerequisites:** Successful deployment of basic prompt management (Phase 6-8).
*   **Tasks:**
    *   [ ] **Database Migration to PostgreSQL:** (Broken down from Hard)
        *   [ ] Set up PostgreSQL development environment (local Docker container). (Easy)
        *   [ ] Create PostgreSQL schema equivalent to SQLite schema. (Easy)
        *   [ ] Update SQLModel session factory for PostgreSQL. (Medium)
        *   [ ] Create migration script to transfer data from SQLite to PostgreSQL. (Medium)
        *   [ ] Test application functionality with PostgreSQL backend. (Medium)
        *   [ ] Update configuration and environment variables. (Easy)
    *   [ ] **API Gateway Setup:** Set up Kong API Gateway (e.g., using Docker). (Medium)
    *   [ ] Configure Kong routes pointing to the FastAPI application. (Medium)
    *   [ ] **Authentication:** Implement API Key Authentication using Kong's `key-auth` plugin. (Medium)
        *   [ ] Define Kong Consumers and associate API keys. (Easy)
        *   [ ] Update API clients/tests to use API keys. (Medium)
    *   [ ] **Rate Limiting:** Configure rate limiting in Kong. (Medium)
    *   [ ] **Containerization:** Containerize the FastAPI application. (Medium)
    *   [ ] **CI/CD Pipeline Implementation:** (Broken down from Hard)
        *   [ ] Set up GitHub Actions workflow for running tests on PR/push. (Medium)
        *   [ ] Create Docker image build and publish workflow. (Medium)
        *   [ ] Set up deployment workflow for staging environment. (Medium)
        *   [ ] Configure environment-specific configurations. (Easy)

### Phase 9: Advanced Prompt Management (v1.2 Features)

*   **Goal:** Implement advanced features requiring PostgreSQL and structured authentication.
*   **Prerequisites:** Phase 5 (PostgreSQL, Kong for Auth).
*   **Tasks:**
    *   [ ] **Implement advanced models and relationships:**
        *   [ ] Extend `Prompt` model with versioning capabilities (parent_id). (Medium)
        *   [ ] Implement `PromptElement` model for structured prompt components. (Medium)
        *   [ ] Implement `PromptTest` model for test case tracking. (Medium)
    *   [ ] **Enhance API endpoints:**
        *   [ ] Add versioning support to existing endpoints. (Medium)
        *   [ ] Implement `GET /prompts/{id}/versions`: Retrieve version history. (Medium)
        *   [ ] Implement `POST /prompts/{id}/test`: Record test results. (Medium)
    *   [ ] **Add advanced business logic:**
        *   [ ] Implement version tracking between related prompts. (Medium)
        *   [ ] Add service logic to record test results and update prompt statistics. (Medium)
    *   [ ] Update API Gateway configuration to protect write endpoints with API key auth. (Easy)

### Phase 10: Embedding Search & Optimization (v1.2+ Features)

*   **Goal:** Implement vector-based search and performance optimizations.
*   **Prerequisites:** Phase 5 (PostgreSQL), Phase 9.
*   **Tasks:**
    *   [ ] **Embedding Search:** (Broken down from Hard)
        *   [ ] Choose vector storage strategy (pgvector, dedicated DB). (Medium)
        *   [ ] Set up vector DB/extension. (Medium)
        *   [ ] Implement SQLModel schema for `PromptEmbedding` with appropriate vector field type. (Medium)
        *   [ ] **Implement embedding generation:** (Broken down from Hard)
            *   [ ] Add OpenAI embeddings client integration. (Medium)
            *   [ ] Create service for batch generation of embeddings. (Medium)
            *   [ ] Implement hooks to update embeddings when prompts change. (Medium)
        *   [ ] Implement `POST /prompts/search/embedding` endpoint. (Medium)
        *   [ ] **Implement vector similarity search:** (Broken down from Hard)
            *   [ ] Create vector query builder for embedding lookups. (Medium)
            *   [ ] Add parameter handling for controlling search specificity. (Medium)
            *   [ ] Implement result ranking and optional filters. (Medium)
    *   [ ] **Monitoring & Optimization:** 
        *   [ ] Integrate with Prometheus/Grafana. (Medium)
        *   [ ] Implement structured logging and aggregation. (Medium)
        *   [ ] Configure Load Balancing for multiple instances. (Medium)
        *   [ ] **Performance Testing & Optimization:** (Broken down from Hard)
            *   [ ] Define load testing scenarios and metrics. (Medium)
            *   [ ] Set up load testing environment and tools. (Medium)
            *   [ ] Execute load tests and identify bottlenecks. (Medium)
            *   [ ] Implement optimization strategies based on findings. (Medium)
        *   [ ] Implement caching strategies if beneficial. (Medium)
