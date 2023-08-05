import setuptools

with open("README.md", 'r') as fh:
    long_description = fh.read()

setuptools.setup(name='scraping',
                 version='0.0.3',
                 description='1st python package',
                 long_description=long_description,
                 long_description_content_type="text/markdown",
                 url='http://github.com/neocxf/py-starter',
                 author='Neo Chen',
                 author_email='neocxf@gmail.com',
                 license='MIT',
                 packages=setuptools.find_packages(),
                 zip_safe=False)
