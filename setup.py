from setuptools import setup, find_packages

setup(
    author='Mooncraft',
    name='pyblitzui',
    install_requires=[
        "flask==1.1.1",
    ],
    version="0.1.0",
    packages=find_packages(exclude=["tests_*", "*example*"]),
    include_package_data=True,
    entry_points="""
    [console_scripts]
    pyblitzui=pyblitzui.launcher:run
    """
)
