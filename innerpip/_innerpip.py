"""
Copyright (c) 2026 Yidong Zhu

Licensed under MIT

"""
import os
import sys
from contextlib import redirect_stdout, redirect_stderr
from typing import overload
from datetime import datetime, timedelta
from innerpip._util import del_module_by_name, ExtendedStringIO


# noinspection SpellCheckingInspection
class Innerpip(object):

  # 日志路径
  __log_path: str | None = None

  @del_module_by_name('logging')
  def __init__(self,
    log_dir: str | None = None,
    auto_del_logs: bool = True,
    days: int = 30
  ) -> None:
    """
    Args:
      log_dir:       日志文件夹
      auto_del_logs: 是否自动删除旧的文件（默认为True）
      days:          保留天数，自动30天

    """
    if log_dir is not None:

      # 创建日志文件夹
      os.makedirs(log_dir, exist_ok=True)

      # 获取当前时间
      now = datetime.now()
      formatted_datetime = now.strftime('%Y%m%d%H%M%S') + now.strftime('%f')[:-3]

      # 日志保存路径
      self.__log_path = os.path.join(log_dir, 'innerpip_%s.log' % formatted_datetime)

      # 删除旧文件
      if auto_del_logs:
        self.delete_old_logs(log_dir, days = days)

    # 尝试导入pip模块，如果导入错误，则安装pip模块
    try:
      import pip
    except ImportError:
      import ensurepip
      ensurepip.bootstrap()
    except Exception as e:
      raise e


  @overload
  @del_module_by_name('logging')
  def __call__(self, args: list[str]): ...
  @overload
  @del_module_by_name('logging')
  def __call__(self, *args: str): ...


  @del_module_by_name('logging')
  def __call__(
    self, *args
  ) -> None:
    """用于调用pip模块main方法"""
    if len(args) == 1 and isinstance(args[0], list):
      self.main(args[0])
    else:
      self.main(list(args))

  def main(self, args: list[str]) -> None:
    """innerpip main方法"""
    if self.__log_path is not None:
      with open(self.__log_path, 'a') as file:
        sync_io = ExtendedStringIO(file, sys.stderr)
        with redirect_stdout(sync_io):
          with redirect_stderr(sync_io):
            import pip
            self.__log(*args, module_name='pip')
            pip.main(args)
    else:
      sync_io = ExtendedStringIO(sys.stderr)
      with redirect_stdout(sync_io):
        with redirect_stderr(sync_io):
          import pip
          self.__log(*args, module_name='pip')
          pip.main(args)


  @staticmethod
  def __log(*msgs: str, module_name: str | None = None) -> None:
    now = datetime.now()
    formatted_datetime = now.strftime('%Y-%m-%d %H:%M:%S.') + now.strftime('%f')[:-3]
    if module_name is not None:
      print(formatted_datetime, f'[{module_name}]', *msgs)
    else:
      print(formatted_datetime, *msgs)


  def delete_old_logs(self, log_dir: str, days: int = 30):
    """
    删除指定文件夹下超过指定天数的文件

    Args:
      log_dir: 日志文件夹路径
      days:    保留天数，默认30天

    """
    with open(self.__log_path, 'a') as file:
      sync_io = ExtendedStringIO(sys.stderr, file)
      with redirect_stdout(sync_io):
        with redirect_stderr(sync_io):

          if not os.path.exists(log_dir):
            print(f"路径不存在: {log_dir}")
            return

          # 1. 计算截止时间点
          now = datetime.now()
          cutoff_date = now - timedelta(days=days)

          deleted_count = 0
          error_count = 0

          # 2. 遍历文件夹
          for root, dirs, files in os.walk(log_dir):
            for filename in files:
              file_path = os.path.join(root, filename)

              try:
                # 3. 获取文件的修改时间
                # os.path.getmtime 返回的是秒级时间戳
                # noinspection SpellCheckingInspection
                file_mtime = os.path.getmtime(file_path)
                file_datetime = datetime.fromtimestamp(file_mtime)

                # 4. 比较时间并删除
                if file_datetime < cutoff_date:
                  os.remove(file_path)
                  self.__log(f'自动删除旧日志: 已删除 {file_path}')
                  deleted_count += 1

              except Exception as e:
                self.__log(f'自动删除旧日志: 删除失败 {file_path}: {e}')
                error_count += 1

          self.__log(f'自动删除旧日志: 处理完成。共删除 {deleted_count} 个文件，{error_count} 个错误。')

