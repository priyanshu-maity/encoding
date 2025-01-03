from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='encoding',
    version='0.1.2',
    author='Priyanshu Maity | Abhineet Bhattacharjee',
    author_email='priyanshu.maity2006@gmail.com | abhineetbhatacharjee@gmail.com',
    description='A package for encoding and decoding text using various ciphers and transformations',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/cup-of-logic/encoding',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
    install_requires=['numpy'],
    include_package_data=True,
    license='MIT'
)
