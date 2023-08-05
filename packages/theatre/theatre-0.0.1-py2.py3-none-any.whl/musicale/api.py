import multiprocessing
import secrets
from functools import wraps
from pathlib import Path
from typing import Union

import zproc

from musicale import exceptions, util
from musicale import processdef
from musicale.constants import *


def start_controller(*, enable_events: bool = False, public: bool = False):
    return multiprocessing.Process(
        target=lambda: processdef.controller(
            util.get_server_address(public), enable_events
        ).main()
    ).start()


def _wrap_cmd_caller(func):
    cmd_name = util.clean_cmd_name(func.__name__)

    @wraps(func)
    def wrapper(self: "MPVClient", *args, **kwargs):

        cmd_args = util.clean_cmd_args(func(self, *args, **kwargs))
        cmd = [cmd_name, *cmd_args]

        return self.call_cmd(cmd)

    return wrapper


class CmdCallerType(type):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)

        for key, val in cls.__dict__.items():
            if not key.startswith("_") and callable(val) and key not in ["call_cmd"]:
                setattr(cls, key, _wrap_cmd_caller(val))

        return cls


class MPVClient(metaclass=CmdCallerType):
    def __init__(self, *, public: bool = False, enable_events: bool = False):
        start_controller(public=public, enable_events=enable_events)

        self._state = zproc.State(
            util.get_server_address(public), namespace=Namespaces.controller
        )

    def call_cmd(self, cmd: list):
        task_id = secrets.token_urlsafe(8)

        self._state["next_cmd"] = cmd, task_id
        result = self._state.get_when_change(task_id)[task_id]

        if isinstance(result, exceptions.MPVException):
            raise result

        return result

    def ignore(self):
        pass

    def seek(
        self,
        seconds: Union[float, int],
        mode: SeekModes.relative,
        precision: SeekPrecisions = None,
    ):
        """
        Change the playback position. By default, seeks by a relative amount of seconds.

        :param seconds:
            The number of seconds to seek.
        :param mode:
            please see :py:class:`SeekModes`.
        :param precision:
            The precision for doing the seek.
            By default, keyframes is used for relative seeks, and exact is used for absolute seeks.

            please see :py:class:`SeekPrecisions` for more.
        :return:
        """
        if precision is not None:
            return seconds, f"{mode.name}+{precision.name}"

        return seconds, mode

    def frame_step(self):
        pass

    def frame_back_step(self):
        pass

    # TODO: Find out WTF ``single`` option in the spec is all about.
    def screenshot(
        self,
        mode: ScreenshotModes = ScreenshotModes.subtitles,
        each_frame: bool = False,
    ):
        """
        Take a screenshot.

        Setting the async flag will make encoding and writing the actual image file asynchronous in most cases.
        (each-frame mode ignores this flag currently.)
        Requesting async screenshots too early or too often could lead to the same filenames being chosen,
        and overwriting each others in undefined order.

        :param mode:
            please see :py:class:`ScreenshotModes`.
        :param each_frame:
            Take a screenshot each frame. Issue this command again to stop taking screenshots.

            .. note::
                You should disable frame-dropping when using this mode -
                or you might receive duplicate images in cases when a frame was dropped.
        :return:
        """
        if each_frame:
            return f"{mode.name}+each_frame"

        return mode

    def screenshot_to_file(
        self,
        filepath: Union[str, Path],
        mode: ScreenshotModes = ScreenshotModes.subtitles,
    ):
        """
        Take a screenshot and save it to a given file.

        The async flag has an effect on this command (see :py:meth:`screenshot`).

        :param filepath:
            The path to the file where the screenshot shall be saved.

            The format of the file will be guessed by the extension
            (and --screenshot-format is ignored - the behavior when the extension is missing or unknown is arbitrary).

            If the file already exists, it's overwritten.

            Like all input command parameters, the filename is subject to
            `Property Expansion <https://mpv.io/manual/master/#property-expansion>`_.
        :param mode:
            please see :py:class:`ScreenshotModes`.
        :return:
        """

        return util.clean_filepath(filepath), mode

    def playlist_next(self, mode: TrackChangeModes = TrackChangeModes.weak):
        """
        Go to the next entry on the playlist.

        :param mode:
            please see :py:class:`TrackChangeModes`.
        :return:
        """
        return mode

    def playlist_prev(self, mode: TrackChangeModes = TrackChangeModes.weak):
        """
        Go to the previous entry on the playlist.

        :param mode:
            please see :py:class:`TrackChangeModes`.
        :return:
        """
        return mode

    # TODO: implement the ``options`` arg from spec
    def loadfile(
        self, filepath: Union[str, Path], mode: LoadFileModes = LoadFileModes.replace
    ):
        """
        Load the given file and play it.

        :param file:
            Path to the track file to be loaded.
        :param mode:
            please see :py:class:`LoadFileModes`.
        :return:
        """
        return util.clean_filepath(filepath), mode

    def loadlist(
        self,
        playlist_path: Union[str, Path],
        mode: LoadListModes = LoadListModes.replace,
    ):
        """
        Load the given playlist file.

        :param playlist_path:
            path to the playlist file.

            Supports some common formats.
            Note that XML playlist formats are not supported.
        :param mode:
            please see :py:class:`LoadListModes`.
        :return:
        """
        return util.clean_filepath(playlist_path), mode

    def playlist_clear(self):
        """Clear the playlist, except the currently played file."""
        pass

    def playlist_remove(self, index: int = None):
        """
        Remove an entry from the playlist.

        :param index:
            Remove the playlist entry at this given index.
            Index values start counting with 0.

            If it is set to ``None``, then remove the **current** entry.

            .. note::
                Removing the current entry also stops playback and starts playing the next entry.

        :return:
        """
        if index is None:
            return "current"

        return index

    def playlist_move(self, index1: int, index2: int):
        """
        Move the playlist entry at ``index1``, so that it takes the place of the entry ``index2``.

        (Paradoxically, the moved playlist entry will not have the index value ``index2`` after moving if index1
        was lower than ``index2``, because ``index2`` refers to the target entry, not the index the entry will have after moving.)
        """
        return index1, index2

    def playlist_shuffle(self):
        """Shuffle the playlist. This is similar to what is done on start if the  --shuffle option is used."""
        pass

    def quit(self, code: int = None):
        """
        Exit the player.

        :param code:
            If this is given, it's used as process exit code.
        """
        if code is not None:
            return code

    def quit_watch_later(self, code: int = None):
        """
        Exit player, and store current playback position.
        Playing that file later will seek to the previous position on start.

        :param code:
            If this is given, it's used as process exit code.
        """
        if code is not None:
            return code

    def sub_add(
        self, mode: AddModes = AddModes.select, title: str = None, lang: str = None
    ):
        """
        Load the given subtitle file. It is selected as current subtitle after loading.

        :param mode:
            please see :py:class:`AddModes`.
        :param title:
            sets the track title in the UI.
        :param lang:
            sets the track language, and can also influence stream selection with flags set to auto.
        :return:
        """
        cmd = [mode]
        if title is not None:
            cmd.append(title)
        if lang is not None:
            cmd.append(title)

        return cmd

    def sub_remove(self, subtitle_id: int = None):
        """
        Remove the given subtitle track. (Works on external subtitle files only.)

        :param subtitle_id:
            If this argument is missing, remove the current track.
        :return:
        """
        if subtitle_id is not None:
            return subtitle_id

    def sub_reload(self, subtitle_id: int = None):
        """
        Reload the given subtitle track. (Works on external subtitle files only.)
        This works by unloading and re-adding the subtitle track.

        :param subtitle_id:
            If this argument is missing, reload the current track.
        :return:
        """
        if subtitle_id is not None:
            return subtitle_id

    def sub_step(self, skip: int):
        """
        Change subtitle timing such, that the subtitle event after the next ``skip`` subtitle events is displayed.
        ``skip`` can be negative to step backwards.
        """
        return skip

    def sub_seek(self, skip: int):
        """
        Seek to the next (``skip`` set to 1) or the previous (``skip`` set to -1) subtitle.

        This is similar to :py:meth:`sub_step`, except that it seeks video and audio instead of adjusting the subtitle delay.

        For embedded subtitles (like with Matroska),
        this works only with subtitle events that have already been displayed, or are within a short prefetch range.
        """
        return skip

    def print_text(self, string: str):
        """
        Print text to stdout. The string can contain properties

        (see `Property Expansion <https://mpv.io/manual/master/#property-expansion>`_).
        """
        return string

    # TODO: Find out wtf is the default value for ``osd_level``
    def show_text(self, string: str, duration_ms: int = 1000, osd_level: int = None):
        """
        Show text on the OSD.

        The string can contain properties, which are expanded as described in
        `Property Expansion <https://mpv.io/manual/master/#property-expansion>`_.

        This can be used to show playback time, filename, and so on.

        :param duration_ms:
            The time in ms to show the message for.
        :param osd_level:
            The minimum OSD level to show the text at.

            0:	OSD completely disabled (subtitles only)
            1:	enabled (shows up only on user interaction)
            2:	enabled + current time visible by default
            3:	enabled + --osd-status-msg (current time and status by default)
        """
        cmd = [string, duration_ms]
        if osd_level is not None:
            cmd.append(osd_level)

        return cmd

    def expand_text(self, string: str):
        """
        Property-expand the argument and return the expanded string.

        See `Property Expansion <https://mpv.io/manual/master/#property-expansion>`_.
        """
        return string

    def show_progress(self):
        """Show the progress bar, the elapsed time and the total duration of the file on the OSD."""
        pass

    def write_watch_later_config(self):
        """Write the resume config file that the quit-watch-later command writes, but continue playback normally."""
        pass

    def stop(self):
        """
        Stop playback and clear playlist.

        With default settings, this is essentially like quit.
        Except that playback can be stopped without terminating the player.
        """
        pass

    def mouse(
        self,
        x: int,
        y: int,
        button: int = None,
        mode: MouseClickModes = MouseClickModes.single,
    ):
        """
        Send a mouse event with given coordinate (``x``, ``y``).

        :param x:
            The X coordinate.
        :param y:
            The Y coordinate.
        :param button:
            The button number of clicked mouse button.
            This should be one of 0-19.

            If this is omitted, only the position will be updated.
        :param mode:
            Only valid if ``button`` is provided.

            please see :py:class:`MouseClickModes`.
        :return:
        """
        cmd = [x, y]
        if button is not None:
            cmd += [button, mode]

        return cmd

    def keypress(self, key_name: str):
        """
        Send a key event through mpv's input handler, triggering whatever behavior is configured to that key.

        :param key_name:
            The key to trigger.

            Uses the `input.conf <https://mpv.io/manual/master/#input-conf>`_ naming scheme for keys and modifiers.
        :return:
        """
        return key_name

    def keydown(self, key_name: str):
        """
        Similar to keypress, but sets the KEYDOWN flag so that if the key is bound to a repeatable command,
        it will be run repeatedly with mpv's key repeat timing until the keyup command is called.

        :param key_name:
            The key to trigger.

            Uses the `input.conf <https://mpv.io/manual/master/#input-conf>`_ naming scheme for keys and modifiers.
        :return:
        """
        return key_name

    def keyup(self, key_name: str = None):
        """
        Set the KEYUP flag, stopping any repeated behavior that had been triggered.


        :param key_name:
            The key to trigger.

            Uses the `input.conf <https://mpv.io/manual/master/#input-conf>`_ naming scheme for keys and modifiers.

            If key_name is not given or is an empty string, KEYUP will be set on all keys.
            Otherwise, KEYUP will only be set on the key specified by ``key_name``.
        :return:
        """
        return key_name

    def audio_add(
        self, mode: AddModes = AddModes.select, title: str = None, lang: str = None
    ):
        """
        Load the given audio file.

        :param mode:
            please see :py:class:`AddModes`.
        :param title:
            sets the track title in the UI.
        :param lang:
            sets the track language, and can also influence stream selection with flags set to auto.
        :return:
        """
        return self.sub_add(mode, title, lang)

    def audio_remove(self, audio_id: int = None):
        """
       Remove the given audio track. (Works on external audio files only.)

        :param audio_id:
            If this argument is missing, remove the current track.
        :return:
        """
        self.sub_remove(audio_id)

    def audio_reload(self, audio_id: int = None):
        """
        Reload the given audio track. (Works on external audio files only.)
        This works by unloading and re-adding the audio track.

        :param audio_id:
            If this argument is missing, reload the current track.
        :return:
        """
        self.sub_reload(audio_id)

    def rescan_external_files(self, mode: SelectionModes = SelectionModes):
        """
        Rescan external files according to the current --sub-auto and --audio-file-auto settings.
         This can be used to auto-load external files after the file was loaded.

        :param mode:
            please see :py:class:`SelectionModes`.
        :return:
        """

    def set(self, prop: str, value):
        """Set the given prop to the given value."""
        return prop, value

    def add(self, prop: str, value=1):
        """
        Add the given value to the prop.

        :param value:
            On overflow or underflow, clamp the prop to the maximum.
        """
        return prop, value

    def cycle(self, prop: str, direction: CycleDirections = CycleDirections.up):
        """
        Cycle the given prop.


        On overflow, set the prop back to the minimum,
        on underflow set it to the maximum.
        """
        return prop, direction

    def multiply(self, prop: str, factor):
        """Multiplies the value of a prop with the numeric factor."""
        return prop, factor

    def client_name(self):
        """
        Return the name of the client as string. This is the string ipc-N with N being an integer number.
        """
        pass

    def get_time_us(self):
        """Return the current mpv internal time in microseconds as a number. This is basically the system time, with an arbitrary offset."""
        pass

    def get_property(self, prop: str):
        """Return the value of the given property. The value will be sent in the data field of the replay message."""
        return prop

    def set_property(self, prop: str, value):
        """Set the given property to the given value. See Properties for more information about properties."""
        return prop, value

    def observe_property(self, prop: str):
        """
        Watch a property for changes.
        """
        return prop

    def unobserve_property(self, event_id: str):
        """
        :param event_id:
        :return:
        """
        return event_id

    def request_log_messages(self):
        """
        Enable output of mpv log messages. They will be received as events. The parameter to this command is the log-level (see mpv_request_log_messages C API function).
        Log message output is meant for humans only (mostly for debugging). Attempting to retrieve information by parsing these messages will just lead to breakages with future mpv releases. Instead, make a feature request, and ask for a proper event that returns the information you need.
        """
        pass

    def enable_event(self, event_name: str):
        """
        Enables or disables the named event. Mirrors the mpv_request_event C API function. If the string all is used instead of an event name, all events are enabled or disabled.
        By default, most events are enabled, and there is not much use for this command.
        """
        return event_name

    def disable_event(self, event_name):
        return event_name

    def get_version(self):
        """Returns the client API version the C API of the remote mpv instance provides."""
        pass
