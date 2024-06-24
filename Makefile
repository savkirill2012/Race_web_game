all: install_serv_dependencies install_front_dependencies

build_server: install_serv_dependencies
	cd src/server/ && gunicorn -b :8000 -k uvicorn.workers.UvicornWorker main:app

build_frontend: install_front_dependencies
	cd src/web_gui/ && npm run dev  

install_front_dependencies:
	cd src/web_gui/ && npm install

install_serv_dependencies:
	cd src/ && poetry install

