import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='finger-print',
    version='0.1.2',
    url='http://github.com/kailashbuki/fingerprint',
    license='LICENSE.txt',
    author='Kailash Budhathoki',
    author_email='kailash.buki@gmail.com',
    description='Document fingerprint generator',
    long_description=long_description,
    packages=['fingerprint'],
    platforms='any',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
)
