import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open('requirements.txt', 'r') as fh:
    install_requires = [line.strip() for line in fh]

print(install_requires)

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
    install_requires=install_requires,
    include_package_data=True,
    package_data={
        '': ['*.txt'],
        'doc': ['*'], 'webapp': ['*']
    }
)
