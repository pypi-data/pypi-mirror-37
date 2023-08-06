#!/user/bin/env python

from distutils.core import setup

setup(
    name='ybc_weather',
    version='1.0.6',
    description='Get The Weather App',
    long_description='Get the weather forecast for the next 15 days',
    author='zhangyun',
    author_email = 'zhangyun@fenbi.com',
    keywords=['pip3', 'weather', 'weathers','python3','python','weather forecast'],
    url='http://pip.zhenguanyu.com/',
    packages=['ybc_weather'],
    packages_data={'ybc_weather': ['*.py']},
    license='MIT',
    install_requires=['requests', 'ybc_config']
)
