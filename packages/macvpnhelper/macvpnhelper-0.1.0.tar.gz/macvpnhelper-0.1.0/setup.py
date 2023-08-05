import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("LICENSE", "r") as li:
    license = li.read()

setuptools.setup(
    name="macvpnhelper",
    version="0.1.0",
    author="Ryan Shea",
    author_email="rshea@aviatainc.com",
    packages=setuptools.find_packages(),
    url="https://github.com/llurkingllama/macvpnhelper/",
    license=license,
    description="Tool to monitor and restart Mac VPN.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    scripts=['bin/macvpnhelper'],
    
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS :: MacOS X",
        "Topic :: Utilities",
        "Topic :: System :: Networking",
        "Natural Language :: English",
        "Development Status :: 4 - Beta"
        "Intended Audience :: End Users/Desktop",
        "Environment :: Console",
        "Environment :: MacOS X",
    ],
    
     #Dependency packages (distributions)
    install_requires=[
        "keyring",
#        "argparse",
#        "getpass",
#        "sys",
#        "subprocess",
#        "time",
#        "datetime",
#        "httplib",
#        "http.client",        
    ],
)
