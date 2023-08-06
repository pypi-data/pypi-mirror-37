import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vampireanalysis",
    version="2.1.0",
    author="Kyu Sang Han",
    author_email="khan21@jhu.edu",
    description="Vampire Image Analysis Package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://wirtzlab.johnshopkins.edu",
    packages=setuptools.find_packages(),
    install_requires=[
        'scipy',
        'pandas',
        'numpy',
        'pillow',
        'matplotlib',
        'scikit-learn',
        'imageio',
        'opencv-python',
    ],
    scripts=['bin/interface-run.py'],
    classifiers=(
        "Programming Language :: Python :: 2.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
    ),
)