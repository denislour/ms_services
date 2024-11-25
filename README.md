# Microservices Architecture

This repository contains a collection of microservices built with Python, FastAPI, and Sanic.

## Services

### Blog Service
A flexible blog microservice with Hexagonal Architecture supporting:
- Multiple frameworks (FastAPI and Sanic)
- Multiple databases (MongoDB and SQLite)
- Domain-Driven Design principles
- Clean Architecture patterns

Features:
- Post management (CRUD operations)
- Comment system
- Status tracking
- Validation and error handling
- Comprehensive test coverage

## Development

### Prerequisites
- Python 3.8+
- Poetry for dependency management
- MongoDB (optional)
- SQLite (optional)

### Setup
1. Clone the repository
```bash
git clone <repository-url>
cd ms_services
```

2. Install dependencies for each service
```bash
cd blog_service
poetry install
```

### Running Tests
```bash
poetry run pytest
```

## Architecture

Each microservice follows these architectural principles:
- Hexagonal Architecture (Ports & Adapters)
- Domain-Driven Design
- SOLID principles
- Clean Architecture
- Test-Driven Development

### Layer Structure
- Domain Layer: Core business logic and entities
- Application Layer: Use cases and ports
- Infrastructure Layer: Database implementations
- Presentation Layer: API endpoints and schemas

## Contributing
1. Create a new branch for your feature
2. Make your changes
3. Write tests
4. Create a pull request

## License
MIT License
