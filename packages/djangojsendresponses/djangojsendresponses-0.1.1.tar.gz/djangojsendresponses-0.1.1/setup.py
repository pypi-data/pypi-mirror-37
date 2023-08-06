import setuptools

setuptools.setup(
    name="djangojsendresponses",
    version="0.1.1",
    url="https://github.com/Ibrohimbek/django-jsend-responses",
    author="Ibrohim Ermatov",
    author_email="ibrohimbek@gmail.com",
    description="Ready Jsend specified response classes.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
