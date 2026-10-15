from setuptools import setup, find_packages

setup(
    name="sq-dev-aigent",
    version="0.1.0",
    description="Local-first supervised AI coding assistant for AndroidIDE Terminal",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={"console_scripts": ["ai=sq_dev_aigent.cli:main"]},
)
