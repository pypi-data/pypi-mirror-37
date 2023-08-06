from setuptools import setup

setup(
    name='d6tjoin',
    version='0.1.1',
    packages=['d6tjoin'],
    url='https://github.com/d6t/d6tjoin',
    license='MIT',
    author='DataBolt Team',
    author_email='support@databolt.tech',
    description='Databolt Python Library',
    long_description='Databolt python library - accelerate data engineering. '
                     'DataBolt provides tools to reduce the time it takes to get your data ready for '
                     'evaluation and analysis.',
    install_requires=[
        'numpy',
        'pandas',
        'jellyfish',
        'joblib'
    ],
    include_package_data=True,
    python_requires='>=3.6'
)
