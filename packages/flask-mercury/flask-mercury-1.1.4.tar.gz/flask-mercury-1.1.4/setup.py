from setuptools import setup, find_packages
# builds the project dependency list
install_requires = None
with open('requirements.txt', 'r') as f:
        install_requires = f.readlines()

# setup function call
setup(
    name="flask-mercury",
    version="1.1.4",
    author="Luis Felipe Muller",
    author_email="luisfmuller@gmail.com",
    description=(
        "Flask-Mercury is a easy to used framework for "
        "implementing and documenting restful APIs based on flask and swagger."
    ),
    keywords="Flask, Swagger, APIs, Rest",
    # Install project dependencies
    install_requires=install_requires,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.txt', '*.rst', '*.md', "*.json", "*.zip", "*.js", "*.css", "*.html", "*.png"],
    },
    include_package_data=True,
    packages=find_packages(exclude=["*tests"])
)
