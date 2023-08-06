from setuptools import setup
setup(
    name='gImageGrabber',
    version='0.0.5',
    author='Saksham Sharma',
    author_email='codeck313@gmail.com',
    packages=['gimagegrabber', 'gimagegrabber.test'],
    scripts=['bin/simpleScript.py'],
    url='https://mysnappy.weebly.com/',
    license='GNU General Public License version 3',
    description='Tool to download orignal resolution images from Google search',
    long_description=open('README.txt').read(),
    install_requires=[
        "urllib3 == 1.23",
        "beautifulsoup4==4.6.3",
        "selenium==3.14.1",

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Natural Language :: English",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Utilities",

    ],
)
