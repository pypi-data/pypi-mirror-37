from setuptools import setup

setup(name='lumby_fbs',
        version='1.0.1',
        description='Lumby flatbuffer schema',
        url='https://github.com/jean-airoldie/lumby-flatbuffers',
        author='Maxence Caron',
        author_email='maxence.caron.1@ulaval.ca',
        license='MIT',
        packages=['lumby_fbs'],
        install_requires=[
            'flatbuffers==1.10'
        ],
        zip_safe=False)
