from distutils.core import setup
ver = '1.0.24'
setup(
    name='gus',
    packages=['gus'],  # this must be the same as the name above
    version=ver,
    description='a python2 git utils',
    author='chang',
    author_email='zhchang@gmail.com',
    url='https://github.com/zhchang/gutils',  # use the URL to the github repo
    download_url='https://github.com/zhchang/gutils/tarball/' + ver,
    keywords=['python', 'git', 'util'],  # arbitrary keywords
    scripts=['scripts/gus'],
    install_requires=[
          'cliapp>=1.0.9',
      ],
    classifiers=[],
)
