from setuptools import setup, find_packages

setup(
    name="rast_common_python",
    version="1.0.0",
    author="Juri Tomak",
    author_email="jtomak@uni-muenster.de",
    license='MIT',
    description="Python classes and functions used in multiple components of our RAST implementation.",
    url="https://github.com/your-username/your-package",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
    ],
)
