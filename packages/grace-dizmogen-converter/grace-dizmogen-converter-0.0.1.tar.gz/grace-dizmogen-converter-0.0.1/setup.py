from setuptools import setup

setup(
    name='grace-dizmogen-converter',
    description='A script to convert grace dizmos to dizmo generator dizmos.',
    author='Michael Diener',
    author_email='mdiener@dizmo.com',
    version='0.0.1',
    scripts=['bin/convert_dizmo'],
    packages=['dizmogen_converter'],
    install_requires=['beautifulsoup4'],
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Environment :: Console'
    ]
)
