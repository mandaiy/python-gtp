from setuptools import setup, find_packages


with open('README.md') as f:
    readme = f.read()


def _read_requirements(filename):
    return open(filename).read().splitlines()


setup(
    name='python-gtp',
    version='0.3.0',
    description='Simple Go Text Protocol wrapper',
    long_description=readme,
    author='Yusaku Mandai',
    author_email='mandai.yusaku@gmail.com',
    url='https://github.com/mandaiy/python-gtp',
    license='Apache 2.0',
    packages=find_packages(exclude=('examples', 'tests')),
    install_requires=_read_requirements('requirements.txt'),
    test_suites='tests'
)
