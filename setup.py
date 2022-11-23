from setuptools import setup

setup(
    name="face-recognition-api",
    version='0.1',
    url='',
    description='',
    author='Justyna Skalska',
    author_email='jastka4@gmail.com',
    packages=["app"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
    ],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ]
)
