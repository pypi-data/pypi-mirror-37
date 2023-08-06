from setuptools import setup, find_packages


setup(
    name='pyatool',
    version='0.1.0',
    description='python android toolkit',
    author='williamfzc',
    author_email='fengzc@vip.qq.com',
    url='https://github.com/williamfzc/pyat',
    packages=find_packages(),
    install_requires=[
        'structlog',
    ]
)
