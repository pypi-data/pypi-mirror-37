import json
from typing import Iterable

import zproc

from musicale import exceptions
from musicale import util
from musicale.constants import Namespaces


def event_processor(state: zproc.State, ipc_path: str):
    state.namespace = Namespaces.event_processor
    _, sock_file = util.get_mpv_client_sock(ipc_path)

    while True:
        msg = sock_file.readline()
        # might not be utf-8, see https://mpv.io/manual/master/#json-ipc
        msg = json.loads(msg.decode())
        util.response_err_check(msg)

        try:
            state["next_event"] = msg["event"]
        except KeyError:
            continue


def controller(
    server_address: str, enable_events: bool = False, mpv_args: Iterable[str] = None
):
    if mpv_args is None:
        mpv_args = []

    ipc_path = util.launch_mpv(*mpv_args)
    sock, sock_file = util.get_mpv_client_sock(ipc_path)

    zproc.start_server(server_address)
    ctx = zproc.Context(server_address, namespace=Namespaces.controller)
    state = ctx.state

    if enable_events:
        ctx.process(
            event_processor, args=[ipc_path], namespace=Namespaces.event_processor
        )

    while True:
        snapshot = state.get_when_change("next_cmd")
        cmd, task_id = snapshot["next_cmd"]

        try:
            result = util.mpv_send_recv(sock, sock_file, cmd)
        except exceptions.MPVException as e:
            result = e

        state[task_id] = result
