from setuptools import setup
 
setup(
    name='Midterm',
    version='0.1',
    description='Programming Languages Mid-Term',
    author='Edsel Norwood',
    author_email='ebnorwood538@students.ecsu.edu',
    install_requires=["numpy >= 1.10", "biopython >= 1.10"],
    packages=['myMidterm', ],
    package_dir={'':'src'},
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=['src/main',],
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README').read(),
    classifiers=[
      'Development Status :: 4 - Beta',
      'Environment :: X11 Applications :: GTK',
      'Intended Audience :: End Users/Desktop',
      'Intended Audience :: Developers',
      'License :: OSI Approved :: GNU General Public License (GPL)',
      'Operating System :: POSIX :: Linux',
      'Programming Language :: Python',
      'Topic :: Desktop Environment',
      'Topic :: Text Processing :: Fonts'
      ],
)