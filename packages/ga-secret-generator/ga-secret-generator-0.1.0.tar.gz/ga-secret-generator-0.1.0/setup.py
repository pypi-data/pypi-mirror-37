from setuptools import setup

setup(
    name='ga-secret-generator',
    author='Andre Keller',
    author_email='andre.keller@vshn.ch',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: System :: Systems Administration',
    ],
    description='generats a google authenticator totp secret',
    entry_points={
        'console_scripts': [
            'ga-secret-generator = ga_secret_generator:main'
        ]
    },
    install_requires=[
        'pyqrcode',
        'pypng',
    ],
    python_requires='>=3.4',
    # BSD 3-Clause License:
    # - http://opensource.org/licenses/BSD-3-Clause
    license='BSD',
    packages=['ga_secret_generator'],
    version='0.1.0',
)
