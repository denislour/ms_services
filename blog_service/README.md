# Blog Service

A flexible blog service built with Hexagonal Architecture, supporting multiple web frameworks and databases.

## 🛠️ Features

- Multiple web framework support:
  - FastAPI
  - Sanic
- Multiple database support:
  - SQLite
  - MongoDB
- Hexagonal Architecture
- Development mode with auto-reload
- Rich CLI interface

## 📋 Requirements

- Python 3.8+
- Poetry for dependency management

## 🚀 Installation

1. Install Poetry (if not already installed):
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

2. Clone the repository:
```bash
git clone <repository-url>
cd blog_service
```

3. Install dependencies:
```bash
poetry install
```

## 💻 Usage

The blog service can be run with different configurations using the CLI:

### View Help
```bash
poetry run blog --help
```

### Basic Run
```bash
# Run with default settings (FastAPI + SQLite)
poetry run blog run

# Run with custom framework and database
poetry run blog run --framework sanic --db mongo

# Run with custom host and port
poetry run blog run --host localhost --port 8080
```

### Development Mode
```bash
# Run with auto-reload (FastAPI + SQLite)
poetry run blog dev

# Run with Sanic and MongoDB
poetry run blog dev --framework sanic --db mongo
```

### Command Options

- Framework (`-f, --framework`):
  - `fastapi` (default)
  - `sanic`

- Database (`-d, --db`):
  - `sqlite` (default)
  - `mongo`

- Host (`--host`):
  - Default: "0.0.0.0"

- Port (`-p, --port`):
  - Default: 8000

- Auto-reload (`-r, --reload`):
  - Enable hot-reloading for development

## 🏗️ Architecture

The project follows Hexagonal (Ports & Adapters) Architecture:

```mermaid
graph TB
    subgraph Presentation[Presentation Layer]
        subgraph Frameworks[Web Frameworks]
            FastAPI[FastAPI Routes]
            Sanic[Sanic Routes]
        end
        Schemas[Pydantic's Schemas]
    end

    subgraph Application[Application Layer]
        UseCases[Use Cases]
        subgraph Ports[Ports]
            InPorts[Input Ports]
            OutPorts[Output Ports]
        end
    end

    subgraph Domain[Domain Layer]
        Entities[Entities]
        ValueObjects[Value Objects]
        DomainServices[Domain Services]
    end

    subgraph Infrastructure[Infrastructure Layer]
        subgraph Adapters[Database Adapters]
            SQLiteAdapter[SQLite Adapter]
            MongoAdapter[MongoDB Adapter]
        end
        Repositories[Repositories]
    end

    subgraph Core[Core Layer]
        Config[Configuration]
        Dependencies[Dependencies]
        subgraph Factories[Factories]
            AppFactory[App Factory]
            DBFactory[DB Factory]
        end
    end

    %% Flow của request
    FastAPI & Sanic --> InPorts
    InPorts --> UseCases
    UseCases --> OutPorts
    UseCases --> Domain
    OutPorts --> Repositories
    Repositories --> Adapters
    
    %% Factory và Dependency Flow
    AppFactory --> Frameworks
    DBFactory --> Adapters
    Factories --> Dependencies
    Dependencies --> UseCases

    %% Styling
    classDef presentation fill:#E1F5FE,stroke:#0288D1,stroke-width:2px
    classDef application fill:#F3E5F5,stroke:#7B1FA2,stroke-width:2px
    classDef domain fill:#FFF3E0,stroke:#EF6C00,stroke-width:2px
    classDef infrastructure fill:#E8F5E9,stroke:#2E7D32,stroke-width:2px
    classDef core fill:#ECEFF1,stroke:#455A64,stroke-width:2px
    
    class Presentation presentation
    class Application application
    class Domain domain
    class Infrastructure infrastructure
    class Core core
```

## 📁 Project Structure

```mermaid
graph TB
    Root[blog_service]
    Application[application/]
    Core[core/]
    Domain[domain/]
    Infrastructure[infrastructure/]
    Presentation[presentation/]

    Root --> Application
    Root --> Core
    Root --> Domain
    Root --> Infrastructure
    Root --> Presentation

    %% Application Layer
    Application --> AppPorts[ports/]
    AppPorts --> UseCases[use_cases/]
    AppPorts --> Repositories[repositories/]

    %% Core Layer
    Core --> Config[config.py]
    Core --> Dependencies[dependencies.py]
    Core --> AppFactory[app_factory.py]
    Core --> DBFactory[db_factory.py]

    %% Domain Layer
    Domain --> Entities[entities/]
    Domain --> ValueObjects[value_objects/]

    %% Infrastructure Layer
    Infrastructure --> SQLite[sqlite3/]
    Infrastructure --> Mongo[mongodb/]
    SQLite --> SQLiteRepo[repositories/]
    SQLite --> SQLiteSession[session.py]
    Mongo --> MongoRepo[repositories/]
    Mongo --> MongoSession[session.py]

    %% Presentation Layer
    Presentation --> API[api/]
    API --> V1[v1/]
    V1 --> Routes[post_router.py]

    %% Styling
    classDef default fill:#f9f,stroke:#333,stroke-width:1px
    classDef layer fill:#fcf,stroke:#333,stroke-width:2px
    class Application,Core,Domain,Infrastructure,Presentation layer
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.
