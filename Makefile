# Nombre del archivo: Makefile

# Variables
VENV=.venv
PYTHON=$(VENV)/Scripts/python
PIP=$(VENV)/Scripts/pip

# Activar entorno y ejecutar la app
run:
	$(VENV)/Scripts/uvicorn app.main:app --reload --port 8002


# Instalar dependencias
install:
	$(PIP) install -r requirements.txt

# Formatear código (opcional)
format:
	$(PYTHON) -m black app

# Ejecutar tests (si tienes pytest configurado)
test:
	$(PYTHON) -m pytest

# Activar entorno virtual (solo referencia)
activate:
	@echo "Para activar el entorno usa:"
	@echo ".venv\\Scripts\\activate" (en Windows)
	@echo "source .venv/bin/activate" (en Linux/Mac)