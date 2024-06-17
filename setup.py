from setuptools import setup, find_packages

# Read the contents of your README file
with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='encoding',  # Your package name
    version='0.1.0',  # Initial release version
    author='Your Name',
    author_email='your.email@example.com',
    description='A package for encoding and decoding text using various ciphers and transformations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/encoding',  # URL to the project repository
    packages=find_packages(),  # Automatically find packages in the project
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[  # List your package's dependencies here
        # e.g., 'numpy', 'requests',
    ],
    include_package_data=True,
    package_data={
        # If any package contains *.txt, *.md, etc. files, include them:
        '': ['*.txt', '*.md'],
    },
    entry_points={
        'console_scripts': [
            # If you have any scripts that should be run as commands, add them here
            # e.g., 'mycommand=mypackage.module:function'
        ],
    },
)
