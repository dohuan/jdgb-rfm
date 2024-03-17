import setuptools
import json

with open("requirements.txt") as requirements_file:
    install_requirements = requirements_file.readlines()

setuptools.setup(
    name="src",
    version="0.0.1",
    author="tech.data.datascience@awesome_company.com.au",
    description="Recency Frequency Montery (RFM)",
    url="https://awesome_company.atlassian.net/wiki/spaces/TD/pages/2732949571/RFM",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_namespace_packages(where=".", include=["src.*"]),
    install_requires=install_requirements,
    python_requires=f">=3.7.10",
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
)
