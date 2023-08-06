from __future__ import absolute_import, division, print_function

from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="django_soc_lite",
    version="0.0.1",
    description="A Powerfull Django plugin to detect and logging Basic Web-based Attack.",
    install_requires=[
        "click==6.6",
        "requests==2.11.1",
        "requests-cache==0.4.13",
        'shellescape==3.4.1'
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    maintainer='threatequation',
    url = "https://github.com/threatequation/django-soc-lite",
    author = "threatequation",
    author_email = "contact@threatequation.com",
    packages=find_packages(),
    package_data={'django_soc_lite': ['rules.json',]},
    include_package_data=True,
    test_suite="django_soc_lite.runtests.runtests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
    ],
)
