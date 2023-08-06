from setuptools import setup

setup(
    name='fe',
    version='0.1dev',
    description='Python Feature engineering (synthesis) for Machine learning',
    author='Musyoka Morris',
    author_email='musyokamorris@gmail.com',
    url='https://github.com/musyoka-morris/fe',
    license='MIT',
    packages=['fe'],
    include_package_data=True,
    requires=[
        'numpy',
        'pandas'
    ]
)
