import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vsmstreamer",
    version="0.1.0",
    author="Praveen Kumar",
    author_email="praveen+pypi@kumar.in",
    description="Cisco Video Surveillance Manager Streamer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kprav33n/vsmstreamer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 2.7",
        "Operating System :: MacOS",
        "License :: OSI Approved :: MIT License",
    ],
    install_requires=[
        'PyCocoa',
        'configparser',
        'python-vlc',
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'vsmstreamer=vsmstreamer:main',
        ],
    }
)
