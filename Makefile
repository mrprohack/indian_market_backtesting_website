.PHONY: test backend frontend dev

test: backend

backend:
	cd backend && PYTHONPATH=. pytest -q

frontend:
	cd frontend && npm run typecheck && npm run build

dev:
	docker compose up --build
