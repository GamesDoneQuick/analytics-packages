try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name="tracker_analytics",
    version="0.1.0",
    description="Analytics tracking library for GDQ's donation tracker and more",
    url="",
    author="",
    author_email="",
    py_modules=["analytics"],
    scripts=["analytics.py"],
    install_requires=[
        "requests>=2.0.0",
        "simplejson>=3.0.0",
    ],
    zip_safe=False,
)
