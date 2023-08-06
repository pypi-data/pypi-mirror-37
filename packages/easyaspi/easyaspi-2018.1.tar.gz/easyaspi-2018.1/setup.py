import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="easyaspi",
    version="2018.1",
    author="Paul Baumgarten",
    author_email="pbaumgarten@gmail.com",
    description="A module intended to abstract away a lot of the complexity of using the GPIO and PiCamera for beginner programmers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/easyaspi",
    packages=setuptools.find_packages(),
    keywords='raspberrypi GPIO picamera beginner',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['rpi.gpio','picamera'],
    python_requires='>=3'
)
