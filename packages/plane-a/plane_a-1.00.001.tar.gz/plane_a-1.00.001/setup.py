from distutils.core import setup
setup(
    name='plane_a',  # 发布的包文件名称
    version='1.00.001',  # 发布的包的版本序号
    description='飞机大战',  # 发布包的描述信息
    author='黑咕隆咚',  # 发布包的作者信息
    author_email='1459025539@qq.com',
    # 作者联系邮箱信息
    py_modules=['__init__', "planeFight"]  # 发布的包中的模块文件列表
)