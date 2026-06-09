"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT

"""
import sys
import io
from typing import TextIO
from typing import Callable, Any


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


class ExtendedStringIO(io.StringIO):

  # 定义多输出
  __outputs: list[TextIO]

  def __init__(self, *sync: TextIO) -> None:
    """
    Args:
      sync:   同步输出流

    Returns:
      return: 无

    """
    # 同步输出到流
    self.__outputs = list(sync)

    # 调用父类构造方法
    super().__init__()


  # 重写write()方法
  def write(self, s: str, /) -> int:

    # 将字符串打印到多输出
    for o in self.__outputs:
      o.write(s)

    # 调用父类write()方法
    return super().write(s)

