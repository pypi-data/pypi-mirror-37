import setuptools

setuptools.setup(
    name="Grank",
    version="0.0.26",
    author="LCTT",
    author_email="xiqingongzi@gmail.com",
    python_requires=">=3.4",
    description="A Github Project Rank Command Line Tool",
    long_description=open('README.rst').read(),
    url="https://github.com/LCTT/Grank",
    project_urls={
        "Bug Tracker": "https://github.com/LCTT/Grank/issues",
        "Documentation": "https://github.com/LCTT/Grank",
        "Source Code": "https://github.com/LCTT/Grank",
    },
    license="GPLv3",
    py_modules=['grank'],
    packages=setuptools.find_packages(),
    install_requires=[
        'click',
        'requests',
        'pandas',
        'numpy',
        'matplotlib'
    ],
    entry_points="""
        [console_scripts]
        grank=grank.core:main
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
)
