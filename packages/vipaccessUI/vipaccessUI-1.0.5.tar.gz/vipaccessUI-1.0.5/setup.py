from setuptools import setup


setup(
    name='vipaccessUI',
    version='1.0.5',
    packages=['vipaccessUI',],
    include_package_data=True,
    url='https://github.com/chris17453/vipaccessUI/',
    license='Creative Commons Attribution-Noncommercial-Share Alike license',
    long_description=open('README.md').read(),
    summary= 'Python UI for TOPF access tokens, provided by vipaccess',
    author= 'Charles Watkins',
    author_email= 'charles@titandws.com',
    description= '',
    platform= 'All',    
    install_requires=["python-vipaccess2"
    ],
    data_files=[
        ('share/icons/hicolor/scalable/apps', ['data/vipaccessUI.svg']),
        ('share/applications', ['data/vipaccessUI.desktop'])
    ],
    entry_points="""
        [console_scripts]
        vipaccessUI = vipaccessUI.main:main
        """    
    
)



