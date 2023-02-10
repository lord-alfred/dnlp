from setuptools import find_packages, setup


setup(
    name='dnlp',
    author='Lord Alfred',
    url='https://github.com/lord-alfred/dnlp',
    license='MIT',
    license_files='LICENSE',
    entry_points={
        'console_scripts': [
            'dnlp=dnlp.app:serve',
        ],
    },
    packages=find_packages('src'),
    package_dir={'': 'src'},
    python_requires='>=3.11',
)
