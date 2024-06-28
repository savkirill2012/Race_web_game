# Race_web_game

Here my realization of simple web race game from BrickGame

# How to start on localhost

server 
port ougth to be 8000
```
make build_server
```

open on different terminal

web
port ougth to be 5173
```
make build_frontend
```

# How to start with docker on localhost

to run docker compose and up 2 containers (for web and server). As in previous case port for server will be 8000 and for web will be 5173.
```
make docker_build
```

to down containers
```
make docker_stop
```


# Start game in web

Open in browser http://localhost:5173/

you will see 

![](./images/web_ui.png)
