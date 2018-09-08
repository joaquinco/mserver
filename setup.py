import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mserver',
    version='0.0.1',
    author='Joaquin Correa',
    author_email='joaquincorrea333@gmail.com',
    description='Web Interface for MPD',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Flask',
        'Natural Language :: Spanish',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Environment :: Web Environment',
        'Topic :: Multimedia :: Sound/Audio',
    ],


    include_package_data=True,
    install_requires=[
        'flask',
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)