import setuptools

setuptools.setup(
    name="mimir_visualizer",
    version="0.0.2",
    author="Steven Hicks",
    author_email="steven@simula.no",
    description="Mimir's visualization module.",
    url="https://github.com/stevenah/mimir-visualizer",
    install_requires=['keras', 'tensorflow', 'opencv-python'],
    packages=setuptools.find_packages(exclude=['tests*', 'examples*']),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)