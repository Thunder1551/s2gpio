from setuptools import setup, find_packages
import os
from subprocess import call

call(["pip3", "install", "git+https://github.com/dpallot/simple-websocket-server.git"])
call(["pip3", "install", "git+https://github.com/giampaolo/psutil.git"])

user = os.listdir("/home")
#pth = '/home/' + user[0]
pth = '/home/pi/'

call(["curl", "-L", "-o", "/home/pi/s2gpio.js", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/s2gpio/s2gpio.js"])
call(["curl", "-L", "-o", "/usr/lib/scratch2/scratch_extensions/s2gpio.js", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/s2gpio/s2gpio.js"])
call(["curl", "-L", "-o", "/usr/lib/scratch2/scratch_extensions/extensions.json", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/additional_files/extensions.json"])
call(["curl", "-L", "-o", "/usr/lib/scratch2/medialibrarythumbnails/mry.png", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/docs/images/mry.png"])


#call(["wget", "-o", "-P", pth, "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/s2gpio/s2gpio.js"])
#call(["wget", "-o", "-P", "/usr/lib/scratch2/scratch_extensions", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/s2gpio/s2gpio.js"])
#call(["wget", "-o", "-P", "/usr/lib/scratch2/scratch_extensions", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/additional_files/extensions.json"])
#call(["wget", "-o", "-P", "/usr/lib/scratch2/medialibrarythumbnails", "https://raw.githubusercontent.com/Thunder1551/s2gpio/master/docs/images/mry.png"])


setup(
    name='s2gpio',
    version='0.1',
    packages=find_packages(),

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
