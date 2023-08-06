import setuptools

def readme():
    try:
        with open('README.md') as f:
            return f.read()
    except IOError:
        return ''


setuptools.setup(
    name="PySimpleGUI27",
    version="1.02.01",
    author="MikeTheWatchGuy",
    author_email="mike@PySimpleGUI.com",
    description="Python 2.7 version of PySimpleGUI - Super-simple to create custom layout GUI's.  80 Demo programs & Cookbook for rapid start.  Examples for Machine Learning(GUI, OpenCV Integration,  Chatterbot), Floating Desktop Widgets, Matplotlib + Pyplot integration, add GUI to command line scripts, PDF & Image Viewer, and more",
    long_description=readme(),
    long_description_content_type="text/markdown",
    keywords="GUI UI tkinter wrapper simple easy beginner novice student graphics progressbar progressmeter",
    url="https://github.com/MikeTheWatchGuy/PySimpleGUI",
    packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Topic :: Multimedia :: Graphics",
        "Operating System :: OS Independent"
    ),
)