import setuptools

description = "Result viewer"

with open("requirements.txt") as fid:
    install_requires = fid.readlines()

setuptools.setup(
    name="result_viewer",
    version="1.0",
    author="Cere",
    author_email="cere@cere.com",
    description=description,
    long_description=description,
    python_requires=">=3.6.0",
    url="https://github.com/Lexcere/ResultViewer",
    install_requires=install_requires,
    package_dir={"result_viewer": "src"},
    packages=["result_viewer", "result_viewer.Plugins"],
    entry_points={
        "console_scripts": ["results = result_viewer.main:main"]
    },
    include_package_data=True,
)
