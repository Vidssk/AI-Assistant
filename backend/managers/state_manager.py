from db.state_db import update_state, get_state
from db.events_db import add_event, get_events
from db.responses_db import add_response, get_latest_response, get_responses
import asyncio

_UNSET = object()

class StateManager:
    def __init__(self, event_bus):
        self.status = "idle"
        self.agent = None
        self.clients = set()
        self.loop = None   # will store FastAPI loop
        self.event_bus = event_bus
        self.system = {
            "cpu": {
                "usage": 0.0,
                "temperature": 0.0
            },
            "gpu": {
                "name": None,
                "usage":0.0,
                "temperature": 0.0,
                "vram_used": 0.0,
                "vram_total": 0.0,
            },
            "memory": {
                "used": 0.0,
                "total":0.0
            },
        }
    def update(
            self, 
            status=None, 
            agent=_UNSET, 
            event=None, 
            cpu=None,
            gpu=None,
            memory=None,
            response=None):
        if status is not None:
            self.status = status
            update_state(status=status)

        if agent is not _UNSET:
            self.agent = agent
            update_state(agent=agent)
        if cpu is not None:
            self.update_system(cpu=cpu)
        if gpu is not None:
            self.update_system(gpu=gpu)
        if memory is not None:
            self.update_system(memory=memory)
        if event:
            add_event(event)
        if response:
            add_response(response, agent=self.agent)

        payload = self.get_payload()
        self.event_bus.emit(payload)

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
            "events": get_events(20),
            "system": self.system,
            "response": get_latest_response(),
            "responses": get_responses(3),
        }
    def update_system(self, cpu=None, gpu=None, memory=None):
        if cpu is not None:
            self.system["cpu"]["usage"] = cpu["usage"]
            self.system["cpu"]["temperature"] = cpu["temperature"]

        if gpu is not None:
            self.system["gpu"]["name"] = gpu["name"]
            self.system["gpu"]["usage"] = gpu["usage"]
            self.system["gpu"]["temperature"] = gpu["temperature"]
            self.system["gpu"]["vram_used"] = gpu["vram_used"]
            self.system["gpu"]["vram_total"] = gpu["vram_total"]

        if memory is not None:
            self.system["memory"]["used"] = memory["used"]
            self.system["memory"]["total"] = memory["total"]



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