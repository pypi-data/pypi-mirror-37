import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dj-loopbreaker",
    version="0.0.1",
    author="Christo Crampton",
    author_email="tech@appointmentguru.co",
    description="Break infinite loops in signals",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/libs/dj-loopbreaker",
    packages=['loopbreaker'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
