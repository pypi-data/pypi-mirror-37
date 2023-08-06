import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subsdata",
    version="0.0.2",
    author="Miguel Ángel Alarcos Torrecillas",
    author_email="miguel.alarcos@gmail.com",
    description="SDP: Subscription Data Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/miguel_alarcos/subsdata/src",
    packages=setuptools.find_packages(),
    install_requires=['rethinkdb==2.3.0.post6', 'PyJWT==1.6.4'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)