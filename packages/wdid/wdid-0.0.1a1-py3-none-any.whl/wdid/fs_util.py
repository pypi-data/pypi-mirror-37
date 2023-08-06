import pathlib
import typing as typ
from functools import lru_cache


@lru_cache(maxsize=2 << 10)
def riterdir(
    path: pathlib.Path, include_dirs: bool = False
) -> typ.Iterator[pathlib.Path]:
    if not path.exists():
        return
    path = path.resolve()
    paths = []
    for subpath in path.iterdir():
        if subpath.is_file():
            paths.append(subpath)
        elif include_dirs and subpath.is_dir():
            paths.append(subpath)
        if subpath.is_dir() and not subpath.is_symlink():
            paths.extend(riterdir(subpath, include_dirs))
    return frozenset(paths)
