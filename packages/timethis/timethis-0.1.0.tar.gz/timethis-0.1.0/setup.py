import setuptools

with open('README.md') as file_object:
    long_description = file_object.read()

setuptools.setup(
    name='timethis',
    version='0.1.0',
    author='Lukas Waymann',
    author_email='meribold@gmail.com',
    description='Context manager for measuring execution times',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/meribold/timethis',
    py_modules=['timethis'],
    python_requires='~=3.6',
)
