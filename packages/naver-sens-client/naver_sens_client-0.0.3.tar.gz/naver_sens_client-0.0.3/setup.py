import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="naver_sens_client",
    version="0.0.3",
    author="santutu",
    author_email="santutu@naver.com",
    description="NAVER SENS CLIENT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/santutu/NaverSensClient",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
