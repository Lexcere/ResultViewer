import setuptools

description = "Result viewer"

# with open("requirements.txt") as fid:
#     install_requires = fid.readlines()

setuptools.setup(
    name="result_viewer",
    version="0.0.1",
    author="Cere",
    author_email="cere@cere.com",
    description=description,
    long_description=description,
    python_requires=">=3.6.0",
    url="https://github.com/Lexcere/ResultViewer",
    install_requires=[
        "numpy",
        "PyQt5",
        "openpyxl",
        "scandir",
        "ConfigParser",
        "colorama"
    ],
    package_dir={"": "src"},
    entry_points={
        "console_scripts": ["results = result_viewer.main:main"]
    },
    include_package_data=True,
)
