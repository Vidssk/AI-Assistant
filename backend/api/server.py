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

    @app.on_event("shutdown")
    async def shutdown():
        event_bus.stop()

    @app.get("/status")
    def status():
        return state_manager.get_payload()

    @app.websocket("/ws")
    async def ws(websocket: WebSocket):
        await websocket.accept()
        clients.add(websocket)

        try:
            await websocket.send_json(state_manager.get_payload())
            while True:
                await websocket.receive_text()
        except WebSocketDisconnect:
            clients.discard(websocket)

    async def broadcaster():
        print("Broadcaster running")

        while True:
            try:
                event = await asyncio.to_thread(event_bus.next_event)
            except RuntimeError:
                break

            if event is None:
                break

            for client in list(clients):
                try:
                    await client.send_json(event)
                except Exception:
                    clients.discard(client)

    return app
