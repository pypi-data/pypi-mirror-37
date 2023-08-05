from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
   name="fabricasdk",
   version="0.1.2",
   description="fabrica sdk",
   long_description=long_description,
   long_description_content_type="text/markdown",
   author="Fabrica Inc.",
   author_email="info@fabrica.city",
   packages=find_packages(),
   package_data={
       "fabricasdk": ["resources/blockchain/**/*.json", "contracts/*"]
   },
   install_requires=[
       "ecdsa==0.13",
       "ipfsapi==0.4.3",
       "requests==2.19.1",
       "rfc3986==1.1.0",
       "web3==4.6.0"
   ]
)
