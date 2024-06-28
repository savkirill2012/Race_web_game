from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from schemas import UserEnvironment, Id
from fastapi.middleware.cors import CORSMiddleware
from race.main_logic import State, updateCurrentState, userInput
import asyncio

app = FastAPI()

origins = ["http://localhost:5173",]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, 
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


class UnicIds():
    def __init__(self):
        self.ids_array = []

    def gen_new_id(self):
        if self.ids_array:
            new_id = self.ids_array[-1] + 1
        else:
            new_id = 1
        self.ids_array.append(new_id)

        return new_id

    def remove_id(self, id: int):
        if id in self.ids_array:
            self.ids_array.remove(id)


gen_ids = UnicIds()


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[UserEnvironment] = []

    async def connect(self, websocket: WebSocket, client_id: int, type: str):
        game_state = State()
        await websocket.accept()
        if type == 'player':
            self.active_connections.append(
                UserEnvironment(game_websocket=websocket,
                                player_websocket=None,
                                client_id=client_id,
                                game_state=game_state)
            )
        elif type == 'game':
            for ws in self.active_connections:
                if ws.client_id == client_id:
                    ws.player_websocket = websocket

    def disconnect(self, websocket: WebSocket, client_id: int):
        for ws in self.active_connections:
            if ws.client_id == client_id:
                gen_ids.remove_id(ws.client_id)
                self.active_connections.remove(ws)

    async def send_state(self, websocket: WebSocket, client_id: int):
        for ws in self.active_connections:
            if ws.client_id == client_id:
                if ws.game_state.pause == 0:
                    ret_val = {str(i): v for i, v in ws.game_state.__dict__.items() if i[0] != '_' and i != 'state_to_default' and i != 'car'}
                    ws.game_state = updateCurrentState(ws.game_state)
                    await ws.game_websocket.send_json(ret_val)
                    await asyncio.sleep(0.5 / ws.game_state.speed)
                    break

    async def catch_state(self, websocket: WebSocket, client_id: int):
        for ws in self.active_connections:
            if ws.client_id == client_id:
                key = await websocket.receive_json()
                if (ws.game_state.pause == 1 and key['key'] == '1') or \
                        ws.game_state.pause == 0:
                    ws.game_state = userInput(int(key['key']), 0, ws.game_state)
                    ret_val = {str(i): v for i, v in ws.game_state.__dict__.items() if i[0] != '_' and i != 'state_to_default' and i != 'car'}
                    await ws.player_websocket.send_json(ret_val)
                break


@app.get('/id')
def send_id():
    return Id(id=gen_ids.gen_new_id())


manager = ConnectionManager()


@app.websocket('/game/{client_id}')
async def ws_game_endpoint(client_id: int, websocket: WebSocket):
    await manager.connect(websocket, client_id, 'game')
    try:
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), 0.001)
            except asyncio.TimeoutError:
                pass
            await manager.send_state(websocket, client_id)
    except WebSocketDisconnect:
        print('clouse game socket')
        manager.disconnect(websocket, client_id)


@app.websocket('/player/{client_id}')
async def ws_player_endpoint(client_id: int, websocket: WebSocket):
    await manager.connect(websocket, client_id, 'player')
    try:
        while True:
            await manager.catch_state(websocket, client_id)
    except WebSocketDisconnect:
        print('clouse player socket')
        manager.disconnect(websocket, client_id)
