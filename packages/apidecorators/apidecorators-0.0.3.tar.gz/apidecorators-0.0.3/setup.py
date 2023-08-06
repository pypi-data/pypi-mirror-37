import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apidecorators",
    version="0.0.3",
    author="Miguel Ángel Alarcos Torrecillas",
    author_email="miguel.alarcos@gmail.com",
    description="API Decorators",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/miguel_alarcos/apidecorators/src",
    packages=setuptools.find_packages(),
    install_requires=['motor>=2.0.0', 'aiohttp>=3.4.4', 'flatten-dict>=0.0.3.post1',
                      'PyJWT>=1.6.4'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest>=3.9.1'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)