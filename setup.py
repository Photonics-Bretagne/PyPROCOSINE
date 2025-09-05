from setuptools import setup, find_packages

setup(
    name="pyprocosine",
    version="0.1.0",
    description="PROCOSINE analysis and simulation toolkit",
    author="Mathieu Ribes, Sofian Helmer, Gaspard Russias",
    author_email="grussias@photonics-bretagne.com",
    packages=find_packages(include=["pyprocosine", "pyprocosine.*"]),
    include_package_data=True,
    package_data={
        "pyprocosine.core": ["dataSpec_P5B.npy"],  # Fichier embarqué dans le package
    },
    install_requires=[
        "Flask==3.1.0",
        "matplotlib==3.8.0",
        "numpy==1.24.4",
        "pandas==2.2.3",
        "scipy==1.9.0",
        "uncertainties==3.1.7"
    ],
    python_requires=">=3.8",
)