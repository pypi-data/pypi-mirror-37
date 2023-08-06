import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='poq',
    version='0.1.1',
    author='poq',
    author_email='emerstar.819eff8@m.yinxiang.com',
    description='An example for teaching how to publish a Python package',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/p2i/poq',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
