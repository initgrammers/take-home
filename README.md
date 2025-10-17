# Backend

## Architecture (Hexagonal)
This backend follows a Hexagonal Architecture (Ports & Adapters), consistent with InitGrammers projects.

- Domain (core business): pure entities and repository interfaces under `backend/src/*/domain` (e.g., Room, Reservation, Payment; RoomRepository, ReservationRepository, PaymentRepository).
- Application (use cases): orchestration of domain rules under `backend/src/*/application` (e.g., ListRoomsUseCase, CreateReservationUseCase, CancelReservationUseCase, ListPaymentsUseCase).
- Infrastructure (adapters): persistence and framework integrations under `backend/src/*/infra` and `backend/api/routes`.
  - Persistence: SQLAlchemy models (RoomModel, ReservationModel, PaymentModel) and PSQL repositories (RoomRepositoryPsql, ReservationRepositoryPsql, PaymentRepositoryPsql).
  - Transport/UI: FastAPI routes in `backend/api/routes` act as driving adapters.
  - DB ops: Alembic migrations and initial data seeding in `backend/src/shared/infra/seed.py`.
- Dependency rule: outer layers depend on inner layers; domain/application do not depend on infrastructure. Infra implements the ports (interfaces) defined in domain.
- Benefits: testability, separation of concerns, and replaceable adapters (e.g., swap database or add transports without changing core).

## Requirements
- Docker and Docker Compose

## Start the backend (Docker)
1. Build and start services:
   - `docker compose up -d --build`
2. API available:
   - http://localhost:8000/docs
3. Database (PostgreSQL):
   - Published on host: `localhost:5433`
   - Internal (Docker network): the `api` service connects to `db:5432`.

Notes:
- The `api` service automatically runs `alembic upgrade head` before starting the server, so migrations are applied on startup.

## Migrations
- Automatic: applied when `api` starts.
- Manual (inside the `api` container):
  1. `docker compose exec api bash`
  2. In `/app`, create a migration for model changes:
     - `alembic revision --autogenerate -m "describe changes"`
  3. Apply migrations:
     - `alembic upgrade head`

## Test endpoints and data
The application exposes REST endpoints and Swagger documentation:
- Documentation: http://localhost:8000/docs

Seeded rooms (default):
- IDs:
  - `7c79f442-fde0-4ef2-9eeb-0dffe92b3a0e` (room1, 80.00)
  - `df2a67e2-cd30-42de-b3be-ee3d4fc24652` (room2, 90.00)
  - `e4ec572e-fc15-44a8-bde5-8e692acf9279` (room3, 100.00)

Examples (curl):
- List rooms:
  - `curl -s http://localhost:8000/rooms`
- Get a room by ID:
  - `curl -s http://localhost:8000/rooms/7c79f442-fde0-4ef2-9eeb-0dffe92b3a0e`
- Create a reservation:
  - `curl -s -X POST http://localhost:8000/reservations -H 'Content-Type: application/json' -d '{"id":"rsv-001","room_id":"7c79f442-fde0-4ef2-9eeb-0dffe92b3a0e","guest_email":"john@example.com","start_date":"2025-11-01","end_date":"2025-11-03"}'`
- Cancel a reservation:
  - `curl -s -X POST http://localhost:8000/reservations/rsv-001/cancel`
- List payments:
  - `curl -s http://localhost:8000/payments`

## Database access
- Using `psql` from your host:
  - `psql -h localhost -p 5433 -U hotel -d hotel`
  - User: `hotel`, password: `hotelpass`.

## Local development without Docker (optional)
- By default, it uses SQLite if `DATABASE_URL` is not defined.
1. Install deps in `backend/` (optional if you use a venv):
   - `pip install -r backend/requirements.txt`
2. Run the server:
   - `cd backend && uvicorn main:app --reload`
   - Docs: http://localhost:8000/docs
3. Migrations with local Postgres (if you define `DATABASE_URL`):
   - `export DATABASE_URL='postgresql+psycopg2://user:pass@host:port/db'`
   - `cd backend && alembic revision --autogenerate -m "changes" && alembic upgrade head`

## Frontend (Next.js)

### Requirements
- Node.js 18+ (recommended)
- Bun

### Run the frontend (development)
1. Install dependencies:
   - `cd frontend/frontend`
   - `bun install`
2. Start the dev server:
   - `bun run dev`
3. Open the app:
   - http://localhost:3000/
4. API proxy:
   - The frontend proxies requests under `/api` to the backend at `http://localhost:8000` (configured via `next.config.ts`). Ensure the backend is running. If you access the app via a LAN IP (e.g., `http://192.168.x.x:3000`), server components construct absolute URLs using request headers, and client components use relative `/api` paths.

### Build for production (optional)
- `bun run build`
- `bun run start`


## Recommendations
- Testing: It is recommended to add automated tests for both backend (domain, application, and integration tests) and frontend (component and end-to-end tests).
- Endpoint documentation: Consider enriching FastAPI endpoint documentation with more detailed responses, examples, tags, and descriptions per endpoint to improve API clarity. Some capabilities provided by FastAPI (e.g., per-endpoint detail) were kept minimal here and can be expanded.
- Availability in calendar: Show a calendar in the reservation flow highlighting AVAILABLE dates and blocking currently reserved dates to avoid invalid selections. Integrate existing reservation periods from the backend and disable occupied ranges.
- UI/UX improvements: Enhance the interface to be more practical and clear (layout, loading/error states, visible validations, feedback messages, responsive design) and apply modern styling to improve the user experience.
