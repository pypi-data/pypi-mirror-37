from setuptools import setup, find_packages


setup(
    name="look",
    version="0.2.2",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="Look",
    long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/tonglei100/look",
    packages=['look'],
    package_data={'look': ['*.py', '*.zip', '*.pkl']},
    install_requires=[
        'visdom',
        'numpy',
        'Pillow'
        ],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3"
    ],
    entry_points={
        'console_scripts': [
            'look=look:example'
        ]    

    }
)
