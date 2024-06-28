DC = docker compose


all: install_serv_dependencies install_front_dependencies

build_server: install_serv_dependencies
	cd src/server/app/ && gunicorn -b :8000 -k uvicorn.workers.UvicornWorker main:app

build_frontend: install_front_dependencies
	cd src/web_gui/ && npm run build
	cd src/web_gui/ && npm run preview

install_front_dependencies:
	cd src/web_gui/ && npm install

install_serv_dependencies:
	cd src/server/ && poetry install

docker_build:
	${DC} -f docker_compose/compose.yaml up -d

docker_stop:
	${DC} -f docker_compose/compose.yaml down  