from setuptools import setup

with open('VERSION') as f:
    version = f.read().strip()

with open('requirements.txt') as f:
    required = f.read().splitlines()

brief_description = """
`https://github.com/brennv/luminol3
<https://github.com/brennv/luminol3>`_.
"""

setup(
    name='luminol3',
    packages=['luminol'],
    version=version,
    description='Anomaly detection for time series data',
    long_description=brief_description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'],
    author='brennv',
    author_email='brennan@beta.build',
    license='Apache 2.0',
    url='https://github.com/brennv/luminol3',
    download_url='https://github.com/brennv/luminol3/tarball/' + version,
    keywords='luminol anomaly detection time series data signal processing',
    install_requires=required,
    include_package_data=True,
    zip_safe=False)
