import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pd_helper',
    version='0.1.6',
    author='Justin Chae',
    author_email='justin@chaemail.com',
    description = 'A helpful script to optimize a Pandas DataFrame.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/justinhchae/pd-helper",
    project_urls={
        "Download URL": "https://github.com/justinhchae/pd-helper/archive/refs/tags/v0.1.6-beta.tar.gz",
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['pandas', 'numpy', 'tqdm', 'shortuuid'],
    python_requires=">=3.7",
)
