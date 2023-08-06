from distutils.core import setup

setup(
    name='ybc_news',
    version='1.1.2',
    description='Get News From juhe API',
    long_description='Get News From juhe API, Contain All Type News',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'news', 'python3', 'python'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_news'],
    package_data={'ybc_news': ['*.py']},  #
    license='MIT',
    install_requires=['requests', 'ybc_config']
)
