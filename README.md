# ECG Analysis Microservice

A FastAPI-based asynchronous microservice for processing and analyzing electrocardiograms (ECGs). This service provides secure endpoints for uploading ECGs and retrieving analytical insights about the signals, leveraging Python's async/await capabilities for efficient I/O operations.

## Getting Started

### Prerequisites

- Docker and Docker Compose installed
- Git

### Local Development Setup

1. Clone the repository  `git clone <repository-url>`
2. Create `.docker.env` file. Copy `.docker.env.example`.
3. Run `bin/server.sh`
4. Create admin user `bin/create_admin.sh  <email> <password>`

## Testing

Tests are written using Pytest with pytest-asyncio for handling asynchronous test cases. The test suite includes both unit tests for data validation and integration tests for API endpoints.

To run tests:
`./bin/tests.sh`


## Features

- **Security**: 
  - JWT-based authentication with access and refresh tokens
  - Password hashing using sha256 with salt
  - Input validation and sanitization using Pydantic models

- **Scalable Architecture**: 
  - API versioning (/api/v1/) allows seamless updates without breaking existing clients
  - Modular design with separate services (auth, analysis) for independent scaling
  - Background task processing with Celery for compute-intensive operations
  - Containerized deployment enables horizontal scaling across multiple instances

## Technical Stack

Core Technologies:
- **Framework**: FastAPI
- **Python Version**: 3.12
- **Database**: PostgreSQL with SQLAlchemy ORM and Alembic for database migrations
- **Package Management**: Poetry for dependency management and packaging

Security & Validation:
- **Authentication**: JWT-based authentication 
- **Data Validation**: Pydantic models

Testing & Development:
- **Testing**: Pytest with pytest-asyncio for asynchronous unit and integration tests
- **Containerization**: Docker for consistent development environments, easy deployment, and scalable infrastructure
- **Development**: Poetry for virtual environment and dependency management

Background Processing:
- **Task Queue**: Celery with RabbitMQ as message broker



## API Endpoints

### Authentication

- `POST /api/v1/auth/register` - Register new users (Admin only)
- `POST /api/v1/auth/login` - User authentication
- `GET /api/v1/auth/refresh` - Refresh access token using refresh token

### ECG Operations

- `POST /api/v1/ecg/` - Upload ECG data
- `GET /api/v1/ecg/{ecg_id}` - Retrieve ECG analysis results


## Future Improvements
Testing Enhancements:

- Add more test cases for data validation and error handling
- Expand test coverage for API endpoints and authentication flows
- Include additional edge case testing

Pre-commit:

- Add pre-commit hooks for automated code quality checks
- Implement automated code formatting with Black and isort
- Add automated linting with Flake8 and Pylint
- Enable type checking with mypy
- Add security scanning with Bandit
- Enforce consistent commit message format
- Add automated test running before commits

GitHub CI/CD:

- Set up GitHub Actions workflow for automated testing

Admin Functionality:

- Add admin user role and permissions system
- Add API endpoints for admin to register new users

Environment Configuration:

- Add development, staging and production environment configurations
- Configure environment-specific settings for databases, caching, etc.
- Set up environment variable management for different deployments



