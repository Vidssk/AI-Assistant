from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio

def create_app(state_manager, event_bus):

    app = FastAPI()

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    clients = set()
    @app.on_event("startup")
    async def startup():
        state_manager.loop = asyncio.get_running_loop()
        asyncio.create_task(broadcaster())
    # @app.on_event("startup")
    # async def startup():
    #     print("Starting broadcaster...")
    #     asyncio.create_task(broadcaster())
    #     print("Broadcaster task created")
    @app.get("/status")
    def status():
        return state_manager.get_payload()
    @app.websocket("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        clients.add(websocket)

        try:
            while True:
                # 1. Always send full state
                await websocket.send_json({
                    "type": "state",
                    "data": state_manager.get_payload()
                })

                # 2. Then try to get an event (non-blocking style)
                try:
                    event = event_bus.queue.get_nowait()
                    await websocket.send_json({
                        "type": "event",
                        "data": event
                    })
                except:
                    pass

                await asyncio.sleep(0.2)

        except WebSocketDisconnect:
            clients.remove(websocket)
    # @app.websocket("/ws")
    # async def ws(websocket: WebSocket):
    #     await websocket.accept()
    #     clients.add(websocket)

    #     try:
    #         while True:
    #             await websocket.receive_text()
    #     except WebSocketDisconnect:
            clients.remove(websocket)

    async def broadcaster():
        print("Broadcaster running")

        while True:
            event = await asyncio.to_thread(event_bus.next_event)

            for client in list(clients):
                try:
                    await client.send_json(event)
                except:
                    clients.discard(client)
    # async def broadcaster():
    #     while True:
    #         event = await asyncio.to_thread(event_bus.next_event)

    #         for client in list(clients):
    #             try:
    #                 await client.send_json(event)
    #             except Exception:
    #                 clients.discard(client)


    return app
# def create_app(state_manager):

#     app = FastAPI()

#     app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
    # @app.on_event("startup")
    # async def startup():
    #     state_manager.loop = asyncio.get_running_loop()
    # @app.get("/")
    # def root():
    #     return {"hello": "world"}

    # @app.get("/status")
    # def status():
    #     return state_manager.get_payload()
    # print("Registering websocket route")
    # @app.websocket("/ws")
    # async def ws(websocket: WebSocket):
    #     await websocket.accept()

    #     state_manager.clients.add(websocket)

    #     try:
    #         while True:
    #             await websocket.receive_text()
    #     except WebSocketDisconnect:
    #         state_manager.clients.remove(websocket)
    # return app
# from fastapi import FastAPI, WebSocket, WebSocketDisconnect
# from fastapi.middleware.cors import CORSMiddleware
# from managers.state_manager import StateManager
# import asyncio

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=[
#         "http://localhost:3000",
#         "http://127.0.0.1:3000"
#     ],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# state = {
#     "status": "idle",
#     "agent": None,
# }

# @app.get("/status")
# def status():
#     return state

# @app.websocket("/ws")
# async def ws_endpoint(websocket: WebSocket):
#     print("Connection attempt")
#     await websocket.accept()
#     print("Connected")

#     try:
#         while True:
#             await websocket.send_json(
#                 state_manager.get_payload()
#             )
#             await asyncio.sleep(0.5)

#     except WebSocketDisconnect:
#         print("Disconnected")


# def set_status(status):
#     state["status"] = status


# def set_agent(agent):
#     state["agent"] = agent