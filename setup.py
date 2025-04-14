from setuptools import find_packages, setup

from hyqt import version


CLASSIFIERS = """
Development Status :: 4 - Beta
Intended Audience :: Developers
Topic :: Software Development :: User Interfaces
License :: OSI Approved :: Apache Software License
""".strip().splitlines()

with open('README.md', encoding='utf8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name         = 'hyqt',
    version      = version,
    author       = 'baiyueheiyu 白月黑羽',
    author_email = 'jcyrss@gmail.com',
    url          = 'https://github.com/jcyrss/hyqt',
    download_url = 'https://pypi.python.org/pypi/hyqt',
    license      = 'Apache License 2.0',
    description  = 'A helper library for python Qt',
    long_description = LONG_DESCRIPTION,
    long_description_content_type = 'text/markdown',
    keywords     = 'hyqt',
    
    python_requires = '>=3.11',
    
    classifiers  = CLASSIFIERS,
    
    # 参考 http://svn.python.org/projects/sandbox/trunk/setuptools/setuptools.txt
    # 参考 https://stackoverflow.com/a/13783919/2602410
    # 参考 https://xebia.com/blog/a-practical-guide-to-using-setup-py/

    #   find_packages() 会从setup.py 所在的目录下面寻找
    #   所有 认为有效的python  package目录（包含 __init__.py 的目录）
    #   然后拷贝加入所有相关的 python 模块文件，但是不包括其他类型的文件
    # packages     = find_packages(),
    packages     = find_packages(
        include = ['hyqt','hyqt.*']
    ),
    
    
    install_requires=[   
        'pyside6',          
    ],
)