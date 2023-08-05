import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="trovotutto",
    version="0.0.1",
    author="Pellegrino Prevete",
    author_email="pellegrinoprevete@gmail.com",
    description="small search engine using k-grams",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/tallero/trovotutto",
    packages=setuptools.find_packages(),
    entry_points = {
        'console_scripts': ['trovotutto = trovotutto:main']
    },
    install_requires=[
        'nltk',
        'pyxdg'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: Unix",
    ],
)
