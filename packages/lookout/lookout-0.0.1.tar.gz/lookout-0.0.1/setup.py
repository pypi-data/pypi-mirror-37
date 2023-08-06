from setuptools import setup, find_packages

setup(
    name="lookout",
    version="0.0.1",
    packages=find_packages(),

    install_requires=[
        "beautifulsoup4>=4.5",
        "feedparser>=5.2",
        "packaging>=17.0",
        "PyGithub>=1.43",
        "requests>=2.19",
    ],

    author="Anonymous Maarten",
    author_email="anonymous.maarten@gmail.com",
    description="API for scanning for new releases of libraries and programs.",
    license="GPLv3+",
    url="https://github.com/madebr/lookout",
    classifiers = [
        "Topic :: System :: Software Distribution",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python :: 3 :: Only  ",
        "Topic :: Software Development",
        "Development Status :: 1 - Planning",
    ]
)
