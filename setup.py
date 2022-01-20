import setuptools

setuptools.setup(
    name="tracker_analytics",
    version="0.1.0",
    description="Analytics tracking library for GDQ's donation tracker and more",
    url="#",
    author="GDQ",
    author_email="",
    packages=setuptools.find_packages(),
    install_requires=[
        "requests>=2.25.1",
        "simplejson>=3.17.3",
    ],
    zip_safe=False,
)
