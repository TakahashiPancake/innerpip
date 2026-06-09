"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT

"""
import sys
from typing import overload, Callable, Any


def del_module_by_name(module_name: str) -> Callable:
  """
  装饰器

  - 根据模块名称删除模块

  Args:
    module_name: 模块名称

  """
  def decorator(func: Callable) -> Callable:
    def wrapper(*args, **kwargs) -> Any:
      # 执行方法
      result = func(*args, **kwargs)
      # 移除模块
      if module_name in sys.modules:
        del sys.modules[module_name]
      return result
    return wrapper
  return decorator


# noinspection SpellCheckingInspection
class Innerpip(object):

  @del_module_by_name('logging')
  def __init__(self) -> None:

    # 尝试导入pip模块，如果导入错误，则安装pip模块
    try:
      import pip
    except ImportError:
      import ensurepip
      ensurepip.bootstrap()
    except Exception as e:
      raise e


  @overload
  def __call__(self, args: list[str]): ...
  @overload
  def __call__(self, *args: str): ...


  def __call__(
    self, *args
  ) -> None:
    if len(args) == 1 and isinstance(args[0], list):
      self.main(args[0])
    else:
      self.main(list(args))

  @del_module_by_name('logging')
  def main(self, args: list[str]) -> None:
    import pip
    pip.main(args)

