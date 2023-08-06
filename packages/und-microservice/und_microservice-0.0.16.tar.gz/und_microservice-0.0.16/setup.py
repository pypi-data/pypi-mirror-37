import setuptools

try: # for pip >= 10
    from pip._internal.req import parse_requirements
except ImportError: # for pip <= 9.0.3
    from pip.req import parse_requirements

from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
    long_description = long_description.replace("\r", "")  # YOU  NEED THIS LINE
except (OSError, ImportError):
    print("Pandoc not found. Long_description conversion failure.")
    import io
    # pandoc is not installed, fallback to using raw contents
    with io.open('README.md', encoding="utf-8") as f:
        long_description = f.read()

requirements = parse_requirements('requirements.txt', session=False)
install_requires = [str(r.req) for r in requirements]

setuptools.setup(
    name="und_microservice",
    author="UND",
    description="UND microservices common utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/und-tech/und-python-microservice",
    install_requires = install_requires,
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
