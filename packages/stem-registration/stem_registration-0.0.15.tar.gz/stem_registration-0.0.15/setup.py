from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="stem_registration",
    version="0.0.15",
    author="Dmitry Shevelev",
    author_email="shevelev.dmitriy@stemsc.com",
    description="A small registration package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.stemsc.com/shevelev/registration",
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'django',
        'django-registration-redux',
        'django-bootstrap4',
        'django-cities-light',
        'django-select2',
    ]
)
