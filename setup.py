import setuptools

setuptools.setup(
    name="cLLiMate",
    version="0.1.0",
    description="A Python package for climate data analysis",
    url="https://github.com/cLLiMate/cLLiMate",
    packages=["cllimate"],
    install_requires=[
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "tqdm",
        "pyarrow",
        "fastapi",
        "gensim",
        "nltk",
        "openai",
        "twilio",
        "python-multipart"
    ],
    extras_require={
        "prod": [
            "uvicorn",
        ]
    },
)
