from setuptools import setup, find_packages

setup(
    name="pyprocosine",
    version="0.1.0",
    description="PROCOSINE analysis and simulation toolkit",
    author="Ton Nom",
    author_email="ton.email@example.com",
    packages=find_packages(include=["pyprocosine", "pyprocosine.*"]),
    include_package_data=True,
    package_data={
        "pyprocosine.core": ["dataSpec_P5B.npy"],  # Fichier embarqué dans le package
    },
    install_requires=[
        # "numpy",
        # "matplotlib",
    ],
    python_requires=">=3.8",
)