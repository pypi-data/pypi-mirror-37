import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="subsdata",
    version="0.0.6",
    author="Miguel Ángel Alarcos Torrecillas",
    author_email="miguel.alarcos@gmail.com",
    description="SDP: Subscription Data Protocol",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/miguel.alarcos/subsdata",
    packages=setuptools.find_packages(),
    install_requires=['rethinkdb>=2.3.0.post6', 'PyJWT>=1.6.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.9.1', 'pytest-asyncio>=0.9.0'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)