import setuptools

with open('README.md', 'r') as f:
    long_description = f.read()

setuptools.setup(
    name='docker-playbook',
    version='0.0.1',
    author='Alex Yang',
    author_email='aleozlx@gmail.com',
    description='YAML driven docker playbook',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'Environment :: Console',
        'License :: OSI Approved :: Apache Software License',
        'License :: OSI Approved :: MIT License',
    ]
)
