from setuptools import setup, find_packages
from jira_ticket_migrate.version import NAME, DESCRIPTION, VERSION


# Parse readme to include in PyPI page
with open("README.md") as f:
    long_description = f.read()


setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mwiens91/jira-ticket-migrate",
    author="Matt Wiens",
    author_email="mwiens91@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "jira-ticket-migrate = jira_ticket_migrate.main:main"
        ]
    },
    python_requires=">=3.6.0",
    install_requires=["jira"],
)
