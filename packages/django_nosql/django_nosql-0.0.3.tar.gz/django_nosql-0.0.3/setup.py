import setuptools

with open("./README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_nosql",
    version="0.0.3",
    author="Christo Crampton",
    author_email="christo@appointmentguru.co",
    description="Stream model updates to nosql backends",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/SchoolOrchestration/django_nosql.git",
    packages=['django_nosql'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
