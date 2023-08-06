from setuptools import setup

setup(
    name='Panzerspiel',
    version='1.00',
    packages=['panzerspiel', ],
    license='GNU General Public License v3.0',
    install_requires=['pygame'],
    description="A small 2D tank game",
    long_description=open('README.md', "r").read(),
    long_description_content_type="text/markdown",
    include_package_data=True,
    package_data={'panzerspiel': ['res2/*.*', 'res2/music/*.mp3']},
    entry_points={
        'console_scripts': ['panzerspiel = panzerspiel.main:main']}
)
