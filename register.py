import inspect, importlib, sys
from pathlib import Path
from typing import Tuple, Iterable, Callable

_DEPENDENCIES = {}

def register_modules_factory(modules: Iterable[str]) -> Tuple[Callable, Callable]:
    """
    Register addon submodules and handle dependency installation
    (if dependencies were added via :func:`add_dependencies`).

    :param list deps: List of module file names to register.
        Each file has to define its own :code:`register()` and :code:`unregister()` functions.
    :return: :code:`register()` and :code:`unregister()` function
    """

    frame = inspect.currentframe()
    try:
        caller_locals = frame.f_back.f_locals
        caller_package = caller_locals["__package__"]
        caller_name = caller_locals["__name__"]

        if dependencies := _DEPENDENCIES.get(caller_name):
            deps, path, no_extra_deps = dependencies

            from ._addon_prefs import get_dependency_addon_prefs
            return get_dependency_addon_prefs(caller_package, deps, path, no_extra_deps)

        _modules = []
        for module in modules:
            if module in caller_locals:
                _modules.append(importlib.reload(caller_locals[module]))
            else:
                _modules.append(importlib.import_module(f".{module}", package=caller_package))

    finally:
        del frame

    def register():
        for module in _modules:
            module.register()

    def unregister():
        for module in reversed(_modules):
            module.unregister()

    return register, unregister

def add_dependencies(deps: dict, path: Path = None, no_extra_deps: bool = False):
    """
    Add dependencies to be installed via pip during registration.

    :param dict deps: Pairs of pip package and module names (can be the same)
    :param pathlib.Path path: Directory to install the dependencies to
        (defaults to ``calling_package_root/site_packages``)
    :param bool no_extra_deps: Ignore any sub-dependencies required (pip --no-deps option)
    """

    frame = inspect.currentframe()
    try:
        caller_locals = frame.f_back.f_locals
        caller_file = caller_locals["__file__"]
        caller_name = caller_locals["__name__"]
    finally:
        del frame

    if not path:
        path = Path(caller_file).parent / "site-packages"
    path = path.resolve()

    if not (path_str := str(path)) in sys.path:
        sys.path.append(path_str)

    importlib.invalidate_caches()

    missing_deps = []
    for dependency, module in deps.items():
        if not importlib.util.find_spec(module):
            missing_deps.append(dependency)

    _DEPENDENCIES.pop(caller_name, None)
    if missing_deps:
        _DEPENDENCIES[caller_name] = (missing_deps, path, no_extra_deps)
