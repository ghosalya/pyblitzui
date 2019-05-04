from setuptools import setup, find_packages

setup(
    author='Mooncraft',
    name='pyblitzui',
    install_requires=[],
    packages=find_packages(exclude=["tests_*", "*example*"]),
    entry_points="""
    [console_scripts]
    pyblitzui=pyblitzui.launcher:run
    """
)
