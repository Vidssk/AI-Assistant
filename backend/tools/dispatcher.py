from managers.app_manager import AppManager
from managers.music_manager import MusicManager
from managers.web_search_manager import WebSearchManager
from managers.file_manager import FileManager
from agents.code_agent import CodeAgent
from agents.chat_agent import ChatAgent


# def handle_general_chat(args):
#     return general_chat(args)

def create_dispatcher(app_manager, chat_agent=None, code_agent=None):
    return {
        "open_app": lambda args: app_manager.open_app(args.get("app")), # Done
        "close_app": lambda args: app_manager.close_app(args.get("app")), # Done
        "play_music": lambda args: MusicManager().play(args.get("query")), # Done
        "search_web": lambda args: WebSearchManager().search(args.get("query")), # Done
        "file_search": lambda args: FileManager().search(args.get("query")),
        "code_help": lambda args: code_agent.handle_code_request(args.get("query")) if code_agent else None,
        "general_chat": lambda args: chat_agent.handle_message(args.get("query")) if chat_agent else None, # Done
    }