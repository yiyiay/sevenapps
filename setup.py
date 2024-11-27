from setuptools import setup, find_packages

setup(
    name="sevenapps",
    packages=find_packages(),
    install_requires=[
        # Prod deps
    ],
    extras_require={
        'test': [
            'pytest>=7.0.0',
            'pytest-cov>=4.0.0',
        ],
    },
) 