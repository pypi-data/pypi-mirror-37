import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="utopia_cli",
    version="1.1.1",
    author="nwmqpa",
    author_email="thomas.nicollet@epitech.eu",
    description="Set of CLIs for managing UtopiaServer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.nwmqpa.com/UtopiaServer/UtopiaInfrastructure/utopiaclis",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    install_requires=['graphcall'],
    entry_points={'console_scripts': [
        'update-server = utopia_cli.server.main:main',
    ]}
)
