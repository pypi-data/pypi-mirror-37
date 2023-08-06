import setuptools

with open("README.md", ) as f:
    long_description = f.read()

setuptools.setup(
    name='proxy-6',
    version='1.0',
    description='Simple api for proxy6.net',
    license="MIT",
    long_description=long_description,
    author='Valentine Bobrovsky',
    author_email='vbabrouski@outlook.com',
    url="https://github.com/vbxx3/proxy6_api",
    packages=['proxy6_api'],  #same as name
    install_requires=["setuptools", "requests"], #external packages as dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
