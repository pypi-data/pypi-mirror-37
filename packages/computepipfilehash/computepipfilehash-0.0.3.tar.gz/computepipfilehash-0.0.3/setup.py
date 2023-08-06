import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="computepipfilehash",
    version="0.0.3",
    author="Kushal Das",
    author_email="mail@kushaldas.in",
    description="To generate requirements file with hashes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3+",
    python_requires=">=3.5",
    url="https://github.com/kushaldas/computepipfilehash",
    packages=setuptools.find_packages(exclude=["docs", "tests"]),
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'computepipfilehash = computepipfilehash:main',
            'sd-downloadsources = computepipfilehash:download_sources',
            'sd-buildwheels = computepipfilehash:build_wheels',
        ],
    },
)
