'''
AUTHOR: YiFoErLiu
VERSION: V1.0.001
DESC: 打包发送邮件模块
'''
from distutils.core import setup


# 具体打包信息
setup(
    name="py18_Email",  # 发布的包文件名称
    version="1.00.001",  # 发布的包的版本序号
    description="注释说明~当前程序包的使用说明",  # 发布包的描述信息
    author="YiFoErLiu",  # 发布包的作者信息
    author_email="937977603@qq.com",  # 作者联系邮箱信息
    py_modules=["__init__","project"]  # 发布的包中的模块文件 列表

)