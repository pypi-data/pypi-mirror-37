import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pywebhdfsme",
    version="0.0.4",
    author="Qu Delin",
    author_email="levinqdl@magicengine.com.cn",
    description="Python wrapper for the Hadoop WebHDFS REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/levinqdl/pywebhdfs/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
    ]
)
