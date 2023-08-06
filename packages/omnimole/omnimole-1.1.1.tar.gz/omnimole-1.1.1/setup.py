from setuptools import setup

setup(
    name='omnimole',

    # Versions should comply with PEP440.
    version='1.1.1',

    description='An image processing toolbox for skin lesion classification',
    long_description='This package is for the image processing code used in the Omnium app. '
                     'The purpose of the app is to detect malignant skin lesions in hopes of '
                     'early diagnosis of skin cancer and melanoma.',
    url='https://github.com/omniumllc/image-processing',
    author='Omnium LLC',
    license='MIT',

    classifiers=[
        # Alpha, Beta, or Production/Stable
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        # 'Topic :: Image Processing :: Mole Classification',
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    keywords='omnium mole lesion image processing',
    packages=['omnimole'],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed.
    install_requires=['imutils',
                      'numpy',
                      'opencv-python',
                      'PyMaxflow',
                      'scikit-image',
                      'scikit-learn'],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'omnimole=omnimole:main',
        ],
    },
)
