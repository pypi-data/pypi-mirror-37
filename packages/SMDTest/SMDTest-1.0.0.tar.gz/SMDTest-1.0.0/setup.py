from setuptools import setup

setup(
    name='SMDTest',
    version='1.0.0',
    description=(
        'calculate the disparity from a stereo image using PSMNet'
    ),
    long_description=open('README.rst').read(),
    author='Faliu',
    author_email='yifaliu86@gmail.com',
    maintainer='Faliu',
    maintainer_email='yifaliu86@gmail.com',
    license='BSD License',
    packages=['PSMNet2','PSMNet2.models','PSMNet2.utils'],
    package_data = {'PSMNet2':['*.tar','models/*','utils/*']},
    exclude_package_data={'PSMNet2':['models','utils']},
    platforms=["all"],
    url='https://github.com/NewBee',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Software Development :: Libraries'
    ],
)
