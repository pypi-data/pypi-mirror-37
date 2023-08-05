from setuptools import setup, find_packages

setup(
    name='applehttp2push',
    version='0.0.3',
    description='一个基于python2和http2的苹果推送SDK，基于yubang的修改。增加文件验证密码',
    author='geyouwen',
    author_email='690591423@qq.com',
    url='https://github.com/geyouwen/applehttp2push',
    packages=find_packages(),
    install_requires=['hyper', ],
)