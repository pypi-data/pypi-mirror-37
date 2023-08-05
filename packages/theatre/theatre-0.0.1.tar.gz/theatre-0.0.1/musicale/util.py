import atexit
import enum
import json
import os
import secrets
import signal
import socket
import struct
import subprocess
from pathlib import Path
from typing import BinaryIO, Tuple, Generator, Union

from musicale import exceptions
from musicale.constants import Namespaces

IPC_BASE_DIR = Path.home() / ".tmp" / "theatre"
if not IPC_BASE_DIR.exists():
    IPC_BASE_DIR.mkdir(parents=True)


def get_mpv_client_sock(ipc_path: str) -> Tuple[socket.socket, BinaryIO]:
    sock = socket.socket(socket.AF_UNIX)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_LINGER, struct.pack("ii", 0, 0))

    while True:
        try:
            sock.connect(ipc_path)
        except (ConnectionError, FileNotFoundError):
            pass
        else:
            break

    return sock, sock.makefile("b")


def launch_mpv(*extra_args: str) -> str:
    ipc_path = IPC_BASE_DIR / Namespaces.controller
    ipc_path = str(ipc_path)

    cmd = [
        "/usr/bin/env",
        "mpv",
        "-idle",
        f"--input-ipc-server={ipc_path}",
        *extra_args,
    ]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pid = proc.pid

    def cleanup(signum, _):
        print("stopped:", pid)
        os.kill(pid, signum)
        os._exit(signum)

    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

    return ipc_path


def response_err_check(msg: dict):
    try:
        error = msg["error"]
    except KeyError:
        pass
    else:
        if error != "success":
            raise exceptions.MPVException(msg)


def mpv_send(sock: socket.socket, cmd: list, request_id: str = None) -> int:
    msg = (
        json.dumps(
            {"command": cmd, "request_id": request_id},
            separators=(",", ":"),
            indent=None,
        )
        + "\n"
    ).encode()

    return sock.send(msg)


def mpv_recv(sock_file: BinaryIO, request_id: str = None) -> dict:
    while True:
        msg = sock_file.readline()
        # might not be utf-8, see https://mpv.io/manual/master/#json-ipc
        msg = json.loads(msg.decode())
        response_err_check(msg)

        if request_id is not None and msg.get("request_id") != request_id:
            continue
        # print(msg)
        return msg.get("data")


def mpv_send_recv(sock: socket.socket, sock_file: BinaryIO, cmd: list) -> dict:
    request_id = secrets.token_urlsafe(8)
    mpv_send(sock, cmd, request_id)
    return mpv_recv(sock_file, request_id)


def mpv_recv_event(sock_file: BinaryIO, event_type: str = None, event_id: str = None):
    while True:
        msg = sock_file.readline()
        # might not be utf-8, see https://mpv.io/manual/master/#json-ipc
        msg = json.loads(msg.decode())
        response_err_check(msg)

        if event_id is not None and msg.get("id") != event_id:
            continue

        if event_type is None or msg.get("event") == event_type:
            try:
                data = msg["data"]
            except KeyError:
                continue

            return data


def mpv_observe(
    sock: socket.socket, sock_file: BinaryIO, prop_to_observe: str
) -> Generator[dict, None, None]:
    event_id = secrets.token_urlsafe(8)
    mpv_send_recv(sock, ["observe_property", event_id, prop_to_observe])
    while True:
        yield mpv_recv_event(sock_file, "property-change", event_id)


CLIENT_API_COMMANDS = [
    "client_name",
    "get_time_us",
    "get_property",
    "get_property_string",
    "set_property",
    "set_property_string",
    "observe_property",
    "observe_property_string",
    "unobserve_property",
    "request_log_messages",
    "enable_event",
    "disable_event",
    "get_version",
]


def clean_cmd_item(item) -> str:
    if isinstance(item, enum.Enum):
        item = item.name

    return item


def clean_cmd_args(cmd_args) -> list:
    if cmd_args is None:
        cmd_args = []
    elif not isinstance(cmd_args, tuple):
        cmd_args = [cmd_args]

    return list(map(clean_cmd_item, cmd_args))


def clean_cmd_name(item: str):
    if item not in CLIENT_API_COMMANDS:
        item = item.replace("_", "-")

    return item


def get_server_address(public: bool = False) -> str:
    if public:
        return "tcp://127.0.0.1:50001"
    else:
        return f'ipc://{str(IPC_BASE_DIR / "player_channel")}'


def clean_filepath(filepath: Union[str, Path]) -> str:
    if not isinstance(filepath, Path):
        filepath = Path(filepath)

    filepath = filepath.expanduser().resolve()

    if not filepath.exists():
        raise FileNotFoundError(f"{repr(filepath)} does not exist.")

    return str(filepath)
