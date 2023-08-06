from setuptools import setup, find_packages


requirements = [
    "requests",
]


setup(
    name='umihico',
    version='0.0.2',
    description="my common functions",
    url='https://github.com/umihico/umihico',
    author='umihico',
    author_email='umihico_dummy@users.noreply.github.com',
    license='MIT',
    keywords='umihico',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)
