from setuptools import setup

setup(
    name='bootsrapzz',
    packages=['bootsrapzz'],
    version='0.7',
    description='Calculate statistical features from text',
    author='Ganes',
    author_email='shivam5992@gmail.com',
    package_data={'': ['data/readme/*.zip']},
    include_package_data=True,
    license='MIT',
    classifiers=(
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        ),
)