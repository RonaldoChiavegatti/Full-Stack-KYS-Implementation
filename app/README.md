
# Fiscal Assistant SaaS for MEIs

A production-ready SaaS platform to help Brazilian Microentrepreneurs (MEIs) with tax declarations, featuring revenue tracking, document OCR, and an AI assistant.

## Features

- **Authentication**: Secure JWT-based login and registration.
- **Dashboard**: Real-time revenue tracking against MEI limits (R$ 81,000/year).
- **Document Management**: Upload invoices/receipts with automatic OCR processing.
- **AI Assistant**: Chat interface powered by Google Gemini for tax questions (RAG).
- **Billing**: Token-based usage tracking and subscription plans.
- **Admin Panel**: User management and system analytics.

## Architecture

The application follows a containerized microservices architecture:

- **Frontend**: Reflex (React wrapper) served via Nginx.
- **Backend**: Reflex (FastAPI) Python application.
- **Database**: PostgreSQL for data persistence.
- **Task Queue**: Redis + Celery for async background tasks (OCR).
- **Storage**: MinIO (S3-compatible) for document storage.

## Technology Stack

- **Language**: Python 3.11+
- **Framework**: Reflex
- **Database**: PostgreSQL, SQLModel
- **AI/ML**: Google Gemini API, Tesseract OCR
- **Infrastructure**: Docker, Docker Compose, Nginx

## Prerequisites

- Docker & Docker Compose
- Google API Key (for AI features)

## Quick Start

1. **Clone the repository**
   bash
   git clone <repository-url>
   cd fiscal-assistant
   

2. **Configure Environment**
   Copy the example environment file and configure your keys:
   bash
   cp app/.env.example .env
   # Edit .env with your settings (especially GOOGLE_API_KEY)
   

3. **Run with Docker Compose**
   To start the full stack:
   bash
   # Note: Deployment files are located in app/ but configured for root execution if moved or referenced correctly.
   # For convenience, you can run:
   docker-compose -f app/docker-compose.yml up --build
   

   The application will be available at `http://localhost`.

## Setup Instructions

### Moving Infrastructure Files (Recommended)
For a standard deployment structure, move the following files from `app/` to the project root:
- `app/Dockerfile`
- `app/docker-compose.yml`
- `app/.env.example`
- `app/.dockerignore`

Then you can simply run `docker-compose up`.

### Database Initialization
The database tables are automatically created by Reflex. To seed initial data:
bash
docker-compose -f app/docker-compose.yml exec app python -m app.scripts.seed_data


## Environment Variables

See `app/.env.example` for a complete list of required variables.

## Development Workflow

1. Install local dependencies:
   bash
   pip install -r requirements.txt
   
2. Run the app in development mode:
   bash
   reflex run
   
3. Access at `http://localhost:3000`.

## Production Deployment

1. Ensure all secrets in `.env` are strong and secure.
2. Update `nginx.conf` with your domain and SSL certificates (Certbot recommended).
3. Run `docker-compose up -d` in your production server.

## Troubleshooting

- **OCR Fails**: Check Celery logs `docker-compose logs celery`. Ensure Tesseract is installed in the worker container.
- **Database Connection**: Ensure PostgreSQL is healthy `docker-compose logs postgres`.
- **MinIO Access**: Check `MINIO_ENDPOINT` matches the container name in Docker network.

## License

Proprietary - All rights reserved.

