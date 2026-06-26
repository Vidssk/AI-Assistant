from db.state_db import update_state, get_state
from db.events_db import add_event, get_events
import asyncio

_UNSET = object()

class StateManager:
    def __init__(self, event_bus):
        self.status = "idle"
        self.agent = None
        self.clients = set()
        self.loop = None   # will store FastAPI loop
        self.event_bus = event_bus
    def update(self, status=None, agent=_UNSET, event=None):
        if status is not None:
            self.status = status
            update_state(status=status)

        if agent is not _UNSET:
            self.agent = agent
            update_state(agent=agent)

        if event:
            add_event(event)

        payload = self.get_payload()
        self.event_bus.emit(payload)

        # # SAFE async bridge
        # if self.loop:
        #     self.loop.call_soon_threadsafe(
        #         lambda: asyncio.create_task(self.broadcast())
        #     )
    # def update(self, status=None, agent=None, event=None):
    # def update(self, status=None, agent=None, event=None):
    #     if status is not None:
    #         self.status = status
    #         update_state(status=status)

    #     if agent is not None:
    #         self.agent = agent
    #         update_state(agent=agent)

    #     if event:
    #         add_event(event)
        
    #     self.event_bus.emit(self.get_payload())
        # if self.loop:
        #     self.loop.call_soon_threadsafe(
        #         lambda: asyncio.create_task(self.broadcast())
        #     )

    # async def broadcast(self):
    #     payload = self.get_payload()

    #     for client in list(self.clients):
    #         try:
    #             await client.send_json(payload)
    #         except:
    #             self.clients.remove(client)
    async def broadcast(self):
        payload = self.get_payload()

        for client in list(self.clients):
            try:
                await client.send_json(payload)
            except:
                self.clients.remove(client)

    def get_payload(self):
        return {
            "status": self.status,
            "agent": self.agent,
            "events": get_events(20)
        }

# class StateManager:
#     def __init__(self):
#         self.status = "idle"
#         self.agent = None

#     def update(self, status=None, agent=None, event=None):

#         if status is not None:
#             self.status = status
#             update_state(status=status)

#         if agent is not None:
#             self.agent = agent
#             update_state(agent=agent)

#         if event:
#             add_event(event)

#         self.broadcast()

#     async def broadcast(self):
#         payload = self.get_payload()

#         for client in self.clients:
#             await client.send_json(payload)

#     def get_payload(self):
#         return {
#             "status": self.status,
#             "agent": self.agent,
#             "events": get_events(20)
#         }
#         # print(payload)
#         # later:
#         # save to sqlite
#         # broadcast websocket

#         # later:
#         # save to sqlite
#         # broadcast websocket