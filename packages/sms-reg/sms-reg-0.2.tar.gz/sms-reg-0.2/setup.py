import setuptools

with open("README.md", ) as f:
    long_description = f.read()

setuptools.setup(
    name='sms-reg',
    version='0.2',
    description=' Python API for sms-reg.com',
    license="MIT",
    long_description=long_description,
    author='Valentine Bobrovsky',
    author_email='vbabrouski@outlook.com',
    url="http://linkedin.com/in/vbxx3",
    packages=setuptools.find_packages(),  # same as name
    install_requires=["setuptools", "requests"],  # external packages as dependencies
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
