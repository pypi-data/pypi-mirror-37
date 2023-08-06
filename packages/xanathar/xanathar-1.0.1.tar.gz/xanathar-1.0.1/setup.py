import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xanathar",
    version="1.0.1",
    author="Max Steinberg",
    author_email="maxssteinberg@gmail.com",
    description="The Xanathar programming Language",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/xanathardevs/xanathar/src/master/",
    packages=setuptools.find_packages(),
    install_requires=['lark-parser', 'llvmlite'],
    data_files=[('grammar', ['xanathar/grammar/GRAMMAR.ebnf']),
                ('stdlib', ['xanathar/stdlib/stdlib.so',
                            'xanathar/stdlib/stdio.so'])],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)