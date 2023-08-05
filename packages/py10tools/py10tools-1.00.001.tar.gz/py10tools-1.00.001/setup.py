# 引入构建包信息的模块
from distutils.core import setup

# 定义发布的包文件的信息
setup(
    name="py10tools",   # 发布包的名称
    version="1.00.001",   # 发布的包的版本序号
    description="我的测试包",   # 发布包的描述信息
    author="小羊咩咩",          # 发布包的作者信息
    author_email="2674635186@qq.com",   # 作者联系邮箱信息
    py_modules=['__init__', 'download', 'engine', 'modules', 'pipelines', 'setup', 'tools', 'utils']   # 发布的包中的模块文件 列表
)

