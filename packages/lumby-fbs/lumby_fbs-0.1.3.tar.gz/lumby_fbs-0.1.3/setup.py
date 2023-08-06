from setuptools import setup

setup(name='lumby_fbs',
        version='0.1.3',
        description='Lumby flatbuffer schema',
        url='https://github.com/jean-airoldie/lumby-flatbuffers',
        author='Maxence Caron',
        author_email='maxence.caron.1@ulaval.ca',
        license='MIT',
        packages=['lumby_fbs'],
        install_requires=[
            'flatbuffers==1.9'
        ],
        zip_safe=False)
