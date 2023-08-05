from setuptools import find_packages, setup


def read_long_description():
    try:
        import pypandoc
        return pypandoc.convert('README.md', 'rst')
    except(IOError, ImportError, RuntimeError):
        return ''


packages = find_packages(exclude=['test_*.py'])

setup(
    name='django_alexa2',
    packages=packages,
    version='0.0.1',
    author='Anton Tuchak',
    author_email='anton.tuchak@gmail.com',
    description='A library ',
    keywords=['amazon alexa'],
    url='https://github.com/atuchak/django-alexa',
    classifiers=[
        'Intended Audience :: Developers',
        'Development Status :: 5 - Production/Stable',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Internet :: WWW/HTTP'
    ],
    install_requires=['requests'],
)
