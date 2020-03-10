from typing import List, Tuple

from mypy.nodes import MypyFile
from mypy.plugin import Plugin


class DepsPlugin(Plugin):
    def get_additional_deps(self, file: MypyFile) -> List[Tuple[int, str, int]]:
        if file.fullname == '__main__':
            return [(10, 'err', -1)]
        return []


def plugin(version):
    return DepsPlugin
