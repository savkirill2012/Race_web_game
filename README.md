# Race_web_game

Here my realization of simple web race game from BrickGame

How to start on localhost

web
port ougth to be 5173
```
cd src/web_gui
npm run dev 
```

server 
port ougth to be 8000
```
cd src/server
gunicorn -k uvicorn.workers.UvicornWorker main:app
```
