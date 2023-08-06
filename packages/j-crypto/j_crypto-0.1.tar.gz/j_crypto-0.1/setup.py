import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="j_crypto",
    version="0.1",
    author="Acciaioli Valverde",
    author_email="acci.valverde@gmail.com",
    description="Helper fucntions to deal with RSA keys",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/foothub/crypto-utils",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
    ],
    scripts=['bin/j-crypto-create-pair'],
    install_requires=['pyjwt', 'cryptography'],
)    
