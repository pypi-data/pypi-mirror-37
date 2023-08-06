import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='iu',
    version='0.0.1',
    author='Dowson',
    author_email='emerstar.819eff8@m.yinxiang.com',
    description='This a package for iu',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/iudata/hello-world',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
