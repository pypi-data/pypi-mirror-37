import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='pysimba',
    version='0.1.0',
    author='Shuangzuan He',
    author_email='zuanzuan1992@gmail.com',
    description='SDK for "https://subway.simba.taobao.com"',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/zuanzuan1992/pysimba',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ]
)
