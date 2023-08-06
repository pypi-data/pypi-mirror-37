from setuptools import setup
setup(
    name='gImageGrabber',
    version='0.0.1',
    author='Saksham Sharma',
    author_email='codeck313@gmail.com',
    packages=['gimagegrabber', 'gimagegrabber.test'],
    scripts=['bin/simpleScript.py'],
    url='https://mysnappy.weebly.com/',
    license='GNU General Public License version 3',
    description='Downloading Orignal Resolution images from Google Search',
    install_requires=[
        "urllib3 == 1.23",
        "beautifulsoup4==4.6.3",
        "selenium==3.14.1",

    ],
)
