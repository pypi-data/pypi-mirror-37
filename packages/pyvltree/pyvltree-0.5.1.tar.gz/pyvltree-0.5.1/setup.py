from setuptools import setup


setup(
    name='pyvltree',
    version='0.5.1',
    author='Daniel Alm Grundström',
    author_email='daniel.alm.grundstrom@protonmail.com',
    packages=[
        'pyvltree',
    ],
    test_suite='pyvltree.test',
    scripts=[],
    url='https://github.com/almgru/pyvl-tree',
    license='LICENSE.txt',
    description='Simple AVL tree implementation.',
    long_description=open('README.rst', 'rt').read(),
    long_description_content_type='text/x-rst',
    install_requires=[],
    python_requires='>=3',
    keywords='tree binary search bst self-balancing avl-tree avl',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',
        'Topic :: Education',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
