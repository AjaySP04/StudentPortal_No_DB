from setuptools import find_packages, setup

setup(
    name='student_nodb',
    version='1.0.0',
    description='Student Portal CRUD app without using any database.',
    url='https://github.com/AjaySP04/StudentPortal_No_DB',
    author='Ajay Singh Parmar',
    author_email='ajays.parmar04@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
                'flask',
                'flask-wtf'
    ],
)
