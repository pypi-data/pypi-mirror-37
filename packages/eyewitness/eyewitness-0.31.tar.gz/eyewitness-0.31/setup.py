from setuptools import setup, find_packages


description = """\
A light weight framework for Object Detection."""

install_requires = [
    'nose2',
    'Pillow',
    'line-bot-sdk',
    'flask',
    'arrow',
    'six',
]


setup(
    name='eyewitness',
    version='0.31',
    description=description,
    author='Ching-Hua Yang',
    url='https://gitlab.com/penolove15/witness',
    install_requires=install_requires,
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True
)
