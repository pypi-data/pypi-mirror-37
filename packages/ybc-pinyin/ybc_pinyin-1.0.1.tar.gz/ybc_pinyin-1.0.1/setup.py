from distutils.core import setup

setup(
    name='ybc_pinyin',
    version='1.0.1',
    description='transform hanzi to pinyin',
    long_description='transform the hanzi to pinyin',
    author='mengxf',
    author_email='mengxf01@fenbi.com',
    keywords=['pip3', 'pinyin', 'python3', 'python', 'pin', 'duoyin'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_pinyin'],
    package_data={'ybc_pinyin': ['*.py']},
    license='MIT',
    install_requires=[
        'pypinyin'
    ]
)