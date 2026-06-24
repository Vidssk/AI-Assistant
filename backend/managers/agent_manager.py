from Jarvis.backend.agents.code_agent import CodeAgent
from Jarvis.backend.agents.chat_agent import ChatAgent
class AgentManager:
    def __init__(self):
        self.agents = {
            "code_agent": CodeAgent(),
            "chat_agent": ChatAgent(),
        }