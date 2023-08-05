from setuptools import setup, find_packages

setup(
    name="django-shutter",
    version="0.9.1",
    license="MIT",
    description="Cloud Photo Toolkit for Django",
    author="Jaco du Plessis",
    author_email="jaco@jacoduplessis.co.za",
    packages=find_packages(),
    package_data={
        'shutter': [
            'templates/shutter/*.html',
        ]
    },
    install_requires=[
        "django",
        "django-allauth",
        "requests",
        "requests-oauthlib",
        "gpxpy",
    ],
)
