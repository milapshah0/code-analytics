.PHONY: setup start stop clean help

help:
	@echo "Usage:"
	@echo "  make setup    - Install dependencies for FE and BE"
	@echo "  make start    - Start both FE and BE locally"
	@echo "  make stop     - Stop all processes"
	@echo "  make clean    - Remove build artifacts and node_modules"

setup:
	@echo "Setting up Backend..."
	cd backend && $(MAKE) setup
	@echo "Setting up Frontend..."
	cd frontend && $(MAKE) setup

start:
	@echo "Starting services..."
	$(MAKE) -j 2 start-be start-fe

start-be:
	cd backend && $(MAKE) start

start-fe:
	cd frontend && $(MAKE) start

stop:
	@echo "Stopping services..."
	-pkill -f "uvicorn"
	-pkill -f "ng serve"

clean:
	cd backend && $(MAKE) clean
	cd frontend && $(MAKE) clean
