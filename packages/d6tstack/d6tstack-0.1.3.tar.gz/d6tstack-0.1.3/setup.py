from setuptools import setup


def read_req(req_file):
    with open(req_file) as req:
        return [line.strip() for line in req.readlines() if line.strip() and not line.strip().startswith('#')]


requirements = read_req('requirements.txt')
requirements_sql = read_req('requirements-sql.txt')
requirements_parquet = read_req('requirements-parquet.txt')

setup(
    name='d6tstack',
    version='0.1.3',
    packages=['d6tstack'],
    url='https://github.com/d6t/d6tstack',
    download_url='https://github.com/d6t/d6tstack/archive/0.1.3.tar.gz',
    license='MIT',
    author='DataBolt Team',
    author_email='support@databolt.tech',
    description='Databolt Python Library',
    long_description='Databolt python library - accelerate data engineering. '
                     'DataBolt provides tools to reduce the time it takes to get your data ready for '
                     'evaluation and analysis.',
    install_requires=requirements,
    extras_require={
        'sql': requirements_sql,
        'parquet': requirements_parquet,
    },
    include_package_data=True,
    python_requires='>=3.6',
    keywords=['d6tstack', 'fast-data-evaluation'],
    classifiers=[]
)
