import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="python_commander",
    version="0.0.6",
    author="Bloodlister",
    author_email="AsenJ.Mihaylov@gmail.com",
    description="A spin-off from Django's manager.py",
    license='MIT',
    long_description=long_description,
    url="https://github.com/Bloodlister/python_commander",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pick'
    ]
)
