from setuptools import setup

setup(
    name='inststd',
    description='..',
    long_description='..',
    version='0.0.4',
    url='https://github.com/guimartino/stdclasses',
    author='Guilherme Martino',
    author_email='gui.martino@hotmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3'
    ],
    packages=['inststd'],
    install_requires=['requests','pip']
)

# rm -rf ~/Library/Caches/pip
# python setup.py sdist bdist_wheel
# git add .
# git commit -m "version"
# git push origin master
# python -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
#!pip install --no-cache-dir --upgrade stdclasses