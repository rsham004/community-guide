
# PromptSculptor API System Diagram

This diagram illustrates the architecture of the PromptSculptor API, including FastAPI internals, Kong as the API Gateway, and interactions with external services.

```mermaid
graph LR
    subgraph External Access
        Clients --> Kong(Kong API Gateway);
    end

    subgraph Gateway Layer
        style Kong fill:#A8E6CF,stroke:#333,stroke-width:2px
        Kong;
    end

    subgraph Backend Application [FastAPI Backend Service]
        direction TB

        subgraph Request Handling
            Router(Endpoints / Routers<br><i>@app.get(...)</i>);
        end

        subgraph Logic Layer
            Service(Services / Business Logic);
        end

        subgraph Data Definition
            Model(Models / Schemas<br><i>Pydantic</i>);
        end

        subgraph Data Access
             DAL(Database Access Layer<br><i>e.g., SQLAlchemy</i>);
        end

        subgraph Auto Documentation
             direction LR
             OpenAPI(OpenAPI Schema<br><i>/openapi.json</i>);
             Swagger(Swagger UI<br><i>/docs</i>);
             ReDoc(ReDoc UI<br><i>/redoc</i>);
        end

        %% Internal Flows
        Router -- Uses --> Model;
        Router --> Service;
        Service -- Uses --> Model;
        Service --> DAL;
        Router -- Generates --> OpenAPI;
        Model -- Defines --> OpenAPI;
        Swagger -- Loads --> OpenAPI;
        ReDoc -- Loads --> OpenAPI;
    end

    subgraph External Dependencies
         direction TB
         DB[(Database<br>e.g., PostgreSQL)];
         style DB fill:#FFD3B6,stroke:#333,stroke-width:2px
         ExtService[(Optional:<br>External Service)];
         style ExtService fill:#B6C8FF,stroke:#333,stroke-width:1px,stroke-dasharray: 5 5
    end

    %% Gateway to Backend/Docs/DB Flows
    Kong -- Routes API Requests --> Router;
    Kong -- Proxies Docs Access --> Swagger;
    Kong -- Proxies Docs Access --> ReDoc;
    DAL --> DB;
    Service --> ExtService;

    %% Styling
    classDef default fill:#f9f9f9,stroke:#333,stroke-width:1px;
    classDef subgraphStyle fill:#eee,stroke:#aaa,stroke-width:1px,color:#333;

    class Clients,Kong,Router,Model,Service,DAL,OpenAPI,Swagger,ReDoc,DB,ExtService default;
    class Backend Application,External Dependencies subgraphStyle;
```
