import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resume_gen",
    version="0.0.2",
    author="Brok Bucholtz",
    description="Generate resumes from template(s) using a person's data.",
    url="https://github.com/Brok-Bucholtz/resume-generator",
    packages=setuptools.find_packages())
