from amino import Dat, List, Maybe, do, Do, Try, Path, Just, Nothing

from ribosome.nvim.io.compute import NvimIO
from ribosome.util.persist import load_json_data, store_json_data
from ribosome.nvim.api.ui import buffers, buffer_name, buflisted, edit_file, current_buffer_name
from ribosome.nvim.api.command import nvim_command
from ribosome.nvim.api.function import nvim_call_tpe
from ribosome.nvim.io.api import N


def is_file(path: Path) -> bool:
    return Try(Path, path).map(lambda a: a.is_file()).true


class BuffersState(Dat['BuffersState']):

    def __init__(self, buffers: List[str], current: Maybe[str]) -> None:
        self.buffers = buffers
        self.current = current


@do(NvimIO[None])
def persist_buffers() -> Do:
    bufs = yield buffers()
    buffer_names = yield bufs.traverse(buffer_name, NvimIO)
    listed = yield bufs.traverse(buflisted, NvimIO)
    files = buffer_names.zip(listed).filter2(lambda n, l: l and is_file(n)).map2(lambda n, l: n)
    current = yield current_buffer_name()
    state = BuffersState(files, Just(current) if is_file(Path(current)) else Nothing)
    yield store_json_data('buffers', state)


@do(NvimIO[None])
def load_buffers(state: BuffersState) -> Do:
    yield state.buffers.traverse(lambda a: nvim_command(f'badd {a}'), NvimIO)
    cmdline_arg_count = yield nvim_call_tpe(int, 'argc')
    if cmdline_arg_count == 0:
        yield state.current.traverse(edit_file, NvimIO)
    yield N.unit


@do(NvimIO[None])
def load_persisted_buffers() -> Do:
    data = yield load_json_data('buffers')
    yield data.cata(lambda a: N.unit, load_buffers)


__all__ = ('persist_buffers', 'load_persisted_buffers',)
