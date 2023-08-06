import os

import setuptools

file_path = os.path.abspath(__file__)
readme = os.path.join(os.path.dirname(file_path), "README.md")
# print(readme)
with open(readme, "r") as fh:
    long_description = fh.read()

setuptools.setup(name='dukepy',
                 description='A useful collection of utilities',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 version='0.0.5',
                 url='https://github.com/duke79/libpython',
                 author='Pulkit Singh',
                 author_email='pulkitsingh01@gmail.com',
                 license='MIT License',
                 classifiers=[
                     "Programming Language :: Python :: 3",
                     "License :: OSI Approved :: MIT License",
                     "Operating System :: OS Independent",
                 ],
                 packages=setuptools.find_packages(),
                 install_requires=[
                     'PyYAML>=3.11',
                     'sh>=1.11'
                 ],
                 entry_points={
                     'console_scripts': [
                         'encrypt=dukepy.main:run'
                     ]
                 }
                 )
