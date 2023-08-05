import setuptools

from LRC.Common.info import version

# get readme description
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="LRC",
    version=version,
    author="Davied Paul",
    author_email="wuwei_543333827@126.com",
    description="A lan remote controller to keyboard associated devices.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/davied9/LANRemoteController",
    packages=setuptools.find_packages(),
    entry_points="""
    [console_scripts]
    lrcclient = LRC.client_main:main
    lrcserver = LRC.server_main:main
    """,
    classifiers=["Programming Language :: Python",],
    setup_requires=['kivy>=1.10.1', 'PyUserInput>=0.1.9']
)
