import setuptools

setuptools.setup(
    name="mimir_visualizer",
    version="0.0.1",
    author="Steven Hicks",
    author_email="steven@simula.com",
    description="Mimir's visualization module.",
    url="https://github.com/stevenah/mimir-visualizer",
    install_requires=['keras', 'tensorflow', 'opencv-python'],
    packages=setuptools.find_packages(exclude=['tests*']),
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)