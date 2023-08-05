from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="airflow-training-operators",
    version="0.0.4",
    author="Bas & Fokko",
    author_email="signal@godatadriven.com",
    description="Apache Airflow components that we use for the Airflow Training material",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/godatadriven/airflow-training-operators",
    packages=find_packages(),
    install_requires=[],
    classifiers=[],
)
