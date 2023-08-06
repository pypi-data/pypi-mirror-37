from setuptools import setup


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='timestamper',
    version='0.0.1',
    py_modules=['timestamper'],
    author='Øystein S. Haaland',
    author_email='oystein@beat.no',
    description="samll helper for recording time usage",
    long_description=readme(),
    url='https://github.com/beat-no/timestamper'
)
