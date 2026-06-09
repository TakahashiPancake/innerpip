# innerpip

### innerpip介绍

innerpip是一个让用户可以在Python脚本中调用pip模块安装所需要的包的工具，并支持输出日志到文件和命令行、自动删除旧的日志

### 使用方法

```python
# 导入Innerpip类
from innerpip import Innerpip

# 实例化Innerpip，并指定日志保存路径
inner_pip = Innerpip(log_dir='./log')

# 执行pip路径

## 第 1 种方法，将Innerpip实例作为方法调用
inner_pip('install', 'pyyaml')
## - 或
inner_pip(['install', 'pyyaml'])

## 第 2 种方法，使用Innerpip.main
inner_pip.main(['install', 'pyyaml'])
```
