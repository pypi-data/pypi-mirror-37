from setuptools import setup

setup(
    name='grace-dizmogen-converter',
    description='A script to convert grace dizmos to dizmo generator dizmos.',
    author='Michael Diener',
    author_email='mdiener@dizmo.com',
    version='0.0.2',
    scripts=['bin/convert_dizmo'],
    packages=['dizmogen_converter'],
    install_requires=['beautifulsoup4'],
    long_description=open('README.md').read(),
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Environment :: Console'
    ]
)
