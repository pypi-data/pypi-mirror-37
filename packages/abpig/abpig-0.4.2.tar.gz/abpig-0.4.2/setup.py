import setuptools

with open('README', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='abpig',
    version='0.4.2',
    description='A Better Python Image Gallery',
    long_description=long_description,
    author='Sean Olson',
    author_email='seandolson654@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'jinja2',
        'Pillow'
    ],
    package_data={
        '': ['index.tmpl']
    }
)
