from setuptools import setup, find_packages

setup(
    name="txt-humanizer",
    version="0.4.0",
    description="Multilingual, dialect-aware AI text detection & humanization framework.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="LangeVC",
    license="Apache-2.0",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "txt-humanizer = txthumanizer.cli:main",
        ],
    },
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Topic :: Text Processing :: Linguistic",
    ],
)
