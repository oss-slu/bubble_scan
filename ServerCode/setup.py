from setuptools import setup, find_packages

setup(
    name="bubble_scan",  # You can name your project
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "Flask",          # Add your dependencies here
        "pytest",
        "opencv-python",
        "numpy"
    ],
)
