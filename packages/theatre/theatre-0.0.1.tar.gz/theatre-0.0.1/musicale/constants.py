import enum


class SeekModes(enum.Enum):
    """
    - relative
        Seek relative to current position (a negative value seeks backwards).
    - absolute
        Seek to a given time (a negative value starts from the end of the file).
    - absolute_percent
        Seek to a given percent position.
    - relative_percent
        Seek relative to current position in percent.
    """

    relative = enum.auto()
    absolute = enum.auto()
    absolute_percent = enum.auto()
    relative_percent = enum.auto()


class SeekPrecisions(enum.Enum):
    """
    - keyframes
        Always restart playback at keyframe boundaries (fast).
    - exact
        Always do exact/hr/precise seeks (slow).
    """

    keyframes = enum.auto()
    exact = enum.auto()


class ScreenshotModes(enum.Enum):
    """
    - subtitles
        Save the video image, in its original resolution, and with subtitles.
        Some video outputs may still include the OSD in the output under certain circumstances.
    - video
        Like subtitles, but typically without OSD or subtitles.
        The exact behavior depends on the selected video output.
    - window
        Save the contents of the mpv window. Typically scaled, with OSD and subtitles.
        The exact behavior depends on the selected video output, and if no support is available, this will act like video.
    """

    subtitles = enum.auto()
    video = enum.auto()
    window = enum.auto()


class TrackChangeModes(enum.Enum):
    """
    - weak
        If the first file on the playlist is currently played, do nothing.
    - force
        Terminate playback if the first file is being played.
    """

    weak = enum.auto()
    force = enum.auto()


class LoadFileModes(enum.Enum):
    """
    - replace
        Stop playback of the current file, and play the new file immediately.
    - append
        Append the file to the playlist.
    - append_play
        Append the file, and if nothing is currently playing, start playback.
        (Always starts with the added file, even if the playlist was not empty before running this command.)
    """

    replace = enum.auto()
    append = enum.auto()
    append_play = enum.auto()


class LoadListModes(enum.Enum):
    """
    - replace
        Stop playback of the current file, and play the new file immediately.
    - append
        Append the file to the playlist.
    """

    replace = enum.auto()
    append = enum.auto()


class AddModes(enum.Enum):
    """
    - select
        Select the subtitle immediately.
    - auto
        Don't select the subtitle. (Or in some special situations, let the default stream selection mechanism decide.)
    - cached
        Select the subtitle.
        If a subtitle with the same filename was already added, that one is selected, instead of loading a duplicate entry.
        (In this case, title/language are ignored, and if the was changed since it was loaded, these changes won't be reflected.)
    """

    select = enum.auto()
    auto = enum.auto()
    cached = enum.auto()


class MouseClickModes(enum.Enum):
    """
    - single
        The mouse event represents regular single click.
    - double
        The mouse event represents double-click.
    """

    single = enum.auto()
    double = enum.auto()


class SelectionModes(enum.Enum):
    """
    - reselect
        Select the default audio and subtitle streams, which typically selects external files with the highest preference.
        (The implementation is not perfect, and could be improved on request.)
    - keep_selection
        Do not change current track selections.
    """

    reselect = enum.auto()
    keep_selection = enum.auto()


class CycleDirections(enum.Enum):
    """
    Sets the cycle direction.
    """

    up = enum.auto()
    down = enum.auto()


class Namespaces:
    controller = "mpv__controller"
    event_processor = "mpv__controller"
