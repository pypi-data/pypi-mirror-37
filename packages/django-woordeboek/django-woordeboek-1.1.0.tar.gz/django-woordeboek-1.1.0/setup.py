from setuptools import setup, find_packages

setup(
    name="django-woordeboek",
    version="1.1.0",
    packages=find_packages(),
    install_requires=[
        "beautifulsoup4",
        "html2text",
        "bleach",
        "requests",
    ],
    package_data={
        'woordeboek': [
            'templates/woordeboek/*.html',
        ]
    },
)
