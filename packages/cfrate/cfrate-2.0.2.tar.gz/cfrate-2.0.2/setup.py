import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cfrate",
    version="2.0.2",
    author="theunderdog",
    author_email="ahmedbonumstelio@gmail.com",
    description="play a file sound - song- once the rating changes at all the participants  of some round. Also if a handle was given the program will output the the changes to that handle",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/theunderdog/Codeforces-rateDetector",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts':['cfrate=cfrate.command:main']
        }
)
