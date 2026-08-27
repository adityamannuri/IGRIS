from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import json
from pathlib import Path
import threading

from command_processor import process_command
from speech_output import speak


HOST = "127.0.0.1"
PORT = 8765
SLEEP_FLAG = Path(__file__).parent / "_igris_sleep.flag"

# Live conversation events
events = []
next_event_id = 1


def add_event(role: str, text: str) -> None:
    """Add a message to the live conversation history."""
    global next_event_id

    events.append(
        {
            "id": next_event_id,
            "role": role,
            "text": text,
        }
    )

    next_event_id += 1

    # Keep only the latest 100 messages.
    if len(events) > 100:
        del events[:-100]


class ConversationHandler(BaseHTTPRequestHandler):

    def send_json(self, status_code: int, data: dict) -> None:
        body = json.dumps(data).encode("utf-8")

        self.send_response(status_code)

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Content-Length",
            str(len(body))
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:
        self.send_response(204)

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, OPTIONS"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.end_headers()

    def do_GET(self) -> None:

        parsed = urlparse(self.path)

        if parsed.path != "/events":
            self.send_json(
                404,
                {"error": "Not found."}
            )
            return

        try:
            query = parse_qs(parsed.query)

            since = int(
                query.get("since", ["0"])[0]
            )

            new_events = [
                event
                for event in events
                if event["id"] > since
            ]

            self.send_json(
                200,
                {
                    "events": new_events
                }
            )

        except Exception as error:
            self.send_json(
                500,
                {
                    "error": str(error)
                }
            )

    def do_POST(self) -> None:

        if self.path == "/shutdown":

            def stop_server():
                self.server.shutdown()

            threading.Thread(
                target=stop_server,
                daemon=True
            ).start()

            self.send_json(
                200,
                {"ok": True}
            )

            return

        parsed = urlparse(self.path)


        # ---------------------------------
        # TYPED CHAT MESSAGE
        # ---------------------------------
        if parsed.path == "/chat":

            try:
                content_length = int(
                    self.headers.get(
                        "Content-Length",
                        "0"
                    )
                )

                raw_body = self.rfile.read(
                    content_length
                )

                data = json.loads(
                    raw_body.decode("utf-8")
                )

                command = str(
                    data.get("message", "")
                ).strip()

                if not command:
                    self.send_json(
                        400,
                        {
                            "error": "Message is empty."
                        }
                    )
                    return

                print(f"You: {command}")

                add_event(
                    "user",
                    command
                )

                response = process_command(command)

                if response == "__SLEEP__":

                    SLEEP_FLAG.write_text(
                    "sleep",
                    encoding="utf-8"
                    )

                    spoken_response = "Going to sleep."

                    add_event(
                    "igris",
                    spoken_response
                    )

                    self.send_json(
                        200,
                        {
                            "response": spoken_response,
                            "sleep": True
                        }
                    )

                    return

                spoken_response = response

                add_event(
                    "status",
                    "SPEAKING"
                )

                add_event(
                    "igris",
                    spoken_response
                )

                speak(spoken_response)

                add_event(
                    "status",
                    "READY"
                )

                add_event(
                    "status",
                    "READY"
                )

                if response != "__SLEEP__":
                     
                    follow_up = "What's now sir?"

                    add_event(
                        "status",
                        "SPEAKING"
                    )

                    follow_up = "What's now sir?"

                    add_event(
                        "status",
                        "SPEAKING"
                        )

                    add_event(
                        "igris",
                        follow_up
                    )

                    speak(follow_up)

                    add_event(
                        "status",
                        "READY"
                    )

                    add_event(
                        "status",
                        "READY"
                    )

                self.send_json(
                    200,
                    {
                        "response": spoken_response,
                        "sleep": response == "__SLEEP__"
                    }
                )

            except Exception as error:

                print(
                    "Conversation server error:",
                    error
                )

                self.send_json(
                    500,
                    {
                        "error": str(error)
                    }
                )

            return

        # ---------------------------------
        # VOICE EVENT
        # ---------------------------------
        if parsed.path == "/event":

            try:
                content_length = int(
                    self.headers.get(
                        "Content-Length",
                        "0"
                    )
                )

                raw_body = self.rfile.read(
                    content_length
                )

                data = json.loads(
                    raw_body.decode("utf-8")
                )

                role = str(
                    data.get("role", "igris")
                ).strip()

                text = str(
                    data.get("text", "")
                ).strip()

                if not text:
                    self.send_json(
                        400,
                        {
                            "error": "Event text is empty."
                        }
                    )
                    return

                add_event(
                    role,
                    text
                )

                self.send_json(
                    200,
                    {
                        "ok": True
                    }
                )

            except Exception as error:

                self.send_json(
                    500,
                    {
                        "error": str(error)
                    }
                )

            return

        self.send_json(
            404,
            {
                "error": "Not found."
            }
        )


def main() -> None:

    server = ThreadingHTTPServer(
        (HOST, PORT),
        ConversationHandler
    )
    server.daemon_threads = True

    print(
        "I.G.R.I.S. conversation bridge running at "
        f"http://{HOST}:{PORT}"
    )

    try:
        server.serve_forever()

    except KeyboardInterrupt:

        print(
            "\nConversation bridge stopped."
        )

    finally:
        server.server_close()


if __name__ == "__main__":
    main()