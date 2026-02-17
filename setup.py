from setuptools import setup

setup(
    name="topsis_jashanpreetsingh_102317065",   # change roll number if needed
    version="0.1",
    author="Jashanpreet Singh",
    author_email="jsingh2_be23@thapar.edu",
    description="A Python package for performing TOPSIS analysis",
    py_modules=["topsis"],
    install_requires=[
        "pandas",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "topsis=topsis:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
