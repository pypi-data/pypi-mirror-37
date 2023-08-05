import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python-flare",
    version="0.0.1",
    author="Michal Cila",
    author_email="michal.cila@cloudevelops.com",
    description="Openstack Flare is a service for running and scheduling burstable task resources.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/openstack/flare",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
