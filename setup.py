from setuptools import setup
import os
from subprocess import call

call(["pip3", "install", "git+https://github.com/dpallot/simple-websocket-server.git"])
call(["pip3", "install", "git+https://github.com/giampaolo/psutil.git"])

user = os.listdir("/home")
pth = '/home/' + user[0]

call(["wget", "-P", pth, "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/s2gpio/s2gpio.js?token=AC3MHLSNSRV25PS4SUBNG6S5PDMLW"])

setup(
    name='s2gpio',
    version='0.1',
    packages=['s2gpio'],

    entry_points={
            'console_scripts': ['s2gpio = s2gpio.s2gpio:run_server',
                                'sbx_to_sb2 = s2gpio.sbx_to_sb2:sbx_to_sb2'],
        },
    url='https://github.com/Thunder1551/s2gpio',
    license='',
    author='',
    author_email='',
    description='',
    keywords=['Raspberry Pi', 'Scratch 2', 'Extensions'],
        classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Environment :: Other Environment',
            'Intended Audience :: Education',
            'License :: ',
            'Operating System :: OS Independent',
            'Programming Language :: Python :: 3.4',
            'Topic :: Education',
            'Topic :: Software Development',
        ],
)
