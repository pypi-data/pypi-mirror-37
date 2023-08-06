from setuptools import setup, find_packages


requirements = [
    "requests",
]
with open('version.txt', 'r') as f:
    version = int(float(f.read()))
version += 1
version = str(version)
with open('version.txt', 'w') as f:
    f.write(version)
version = '.'.join(str(version).zfill(3))

setup(
    name='umihico',
    version=version,
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
