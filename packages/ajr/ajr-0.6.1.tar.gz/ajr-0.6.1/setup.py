from setuptools import setup, find_packages
setup(
    name="ajr",
    version="0.6.1",
    packages=find_packages(),
    install_requires=[],
    author="Close Screen",
    author_email="close.screen@gmail.com",
    description="Asyncronous JSON-RPC router.",
    license="MIT",
    keywords="Async JSON-RPC AIOHTTP",
    url="https://bitbucket.org/closescreen/ajr/src/master/",
    project_urls={
         #"Bug Tracker": "https://bugs.example.com/HelloWorld/",
         #"Documentation": "https://docs.example.com/HelloWorld/",
         "Source Code": "https://bitbucket.org/closescreen/ajr/src/master/",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3.7",
    ]
)