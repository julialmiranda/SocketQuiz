import json
import asyncio
import tornado.web
import tornado.websocket
from server.manager import RoomManager
from core.logger import get_logger

logger = get_logger(__name__)


class CreateRoomHandler(tornado.web.RequestHandler):
    def initialize(self, room_manager: RoomManager) -> None:
        self.room_manager = room_manager

    def get(self) -> None:
        room_id = self.room_manager.create_room()
        link = f"http://localhost:8888/?sala={room_id}"
        self.write({"room_id": room_id, "link": link})


class GameWebSocketHandler(tornado.websocket.WebSocketHandler):
    connections = {}  # sala -> conexões

    def initialize(self, room_manager: RoomManager) -> None:
        self.room_manager = room_manager
        self.room_id = None
        self.player_id = None
        self.player_name = None

    def open(self) -> None:
        self.room_id = self.get_argument("sala", None)

        if not self.room_id:
            self.close()
            return

        room = self.room_manager.get_room(self.room_id)
        if not room:
            self.close()
            return

        self.player_id = str(id(self))
        self.player_name = room.assign_player(self.player_id)

        GameWebSocketHandler.connections.setdefault(self.room_id, []).append(self)

        if self.player_name:
            self.write_message(json.dumps({
                "type": "init",
                "player": self.player_name,
                "room": self.room_id
            }))

            if room.can_start():
                self.broadcast_question(room)
            else:
                self.write_message(json.dumps({
                    "type": "wait",
                    "message": "Aguardando o segundo jogador..."
                }))
        else:
            self.write_message(json.dumps({
                "type": "full",
                "message": "Sala cheia"
            }))
            self.close()

    def on_message(self, message: str) -> None:
        try:
            data = json.loads(message)
            room = self.room_manager.get_room(self.room_id)

            if not room:
                return

            action = data.get("action")

            if action == "answer":
                option = data.get("option")

                if isinstance(option, int) and room.register_answer(self.player_name, option):
                    if room.all_answered():
                        round_result = room.finish_round()
                        self.broadcast_round_result(round_result)

                        async def next_step():
                            await asyncio.sleep(5)

                            if room.state.game_over:
                                self.broadcast_finished(room)
                            else:
                                self.broadcast_question(room)

                        asyncio.create_task(next_step())

        except Exception as e:
            logger.error(f"Erro no WebSocket: {e}")

    def on_close(self) -> None:
        if self.room_id and self.player_id:
            room = self.room_manager.get_room(self.room_id)
            if room:
                room.remove_player(self.player_id)

        if self.room_id in GameWebSocketHandler.connections:
            if self in GameWebSocketHandler.connections[self.room_id]:
                GameWebSocketHandler.connections[self.room_id].remove(self)

            if not GameWebSocketHandler.connections[self.room_id]:
                del GameWebSocketHandler.connections[self.room_id]

    def broadcast_question(self, room) -> None:
        state = room.state.to_dict()
        message = json.dumps({
            "type": "question",
            "state": state
        })

        for handler in GameWebSocketHandler.connections.get(self.room_id, []):
            handler.write_message(message)

    def broadcast_round_result(self, result: dict) -> None:
        message = json.dumps({
            "type": "round_result",
            "correct_option": result["correct_option"],
            "scores": result["scores"]
        })

        for handler in GameWebSocketHandler.connections.get(self.room_id, []):
            handler.write_message(message)

    def broadcast_finished(self, room) -> None:
        state = room.state.to_dict()
        message = json.dumps({
            "type": "finished",
            "state": state
        })

        for handler in GameWebSocketHandler.connections.get(self.room_id, []):
            handler.write_message(message)