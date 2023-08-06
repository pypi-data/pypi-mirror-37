from setuptools import setup, find_packages


setup(
    name="gridder",
    version="1.0.0",
    description="Generate tiles and grids over images.",
    url="https://gitlab.com/brzrkr/gridder",
    author="Federico Salerno",
    author_email="itashadd+gridder@gmail.com",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Utilities",
    ],
    keywords="grid tile tileset image generator",
    packages=find_packages(exclude=['test']),
    install_requires=['Pillow', 'numpy'],
    python_requires=">=3.2",
    project_urls={
        "Source": "https://gitlab.com/brzrkr/gridder",
    },
)
