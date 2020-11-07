import setuptools

setuptools.setup(
    name="bubble",
    version="0.0.1",
    author="Hamish Gibbs",
    author_email="Hamish.Gibbs@lshtm.ac.uk",
    description="CLI tool for scaffolding research projects.",
    url="https://github.com/hamishgibbs/bubble",
    py_modules=['bubble', 'template', 'makefile', 'dockerfile', 'utils'],
    install_requires=[
        'Click',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points='''
        [console_scripts]
        bubble=bubble:cli
    ''',
)
