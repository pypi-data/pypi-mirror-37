try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def version():
    with open('crashlog.py') as fp:
        for line in fp:
            if '__version__' not in line:
                continue
            fields = line.split('=')
            return fields[-1].strip().replace("'", '')


with open('README.md') as fp:
    long_description = fp.read()

setup(
    name='crashlog',
    version=version(),
    description='Log & email uncaught exceptions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Miki Tebeka',
    author_email='miki.tebeka@gmail.com',
    license='MIT',
    url='https://github.com/tebeka/crashlog',
    py_modules=['crashlog'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    tests_require=['pytest'],
)
