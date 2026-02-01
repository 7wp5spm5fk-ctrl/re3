import os
from importlib.machinery import SourceFileLoader
from importlib.util import module_from_spec, spec_from_loader


def _load_impl():
    here = os.path.dirname(__file__)
    impl_path = os.path.join(here, 'VCGXT.PY')
    if not os.path.exists(impl_path):
        raise ImportError(f"无法加载模块: {impl_path}")

    loader = SourceFileLoader('VCGXT_impl', impl_path)
    spec = spec_from_loader(loader.name, loader)
    if spec is None:
        raise ImportError(f"无法加载模块: {impl_path}")
    module = module_from_spec(spec)
    loader.exec_module(module)
    return module


_impl = _load_impl()
VCGXT = _impl.VCGXT

__all__ = ['VCGXT']
