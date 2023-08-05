import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = "GeneMethyl",
    version = "1.0.0",
    author = "Joon-Hyeong Park",
    author_email = "clearclouds@snu.ac.kr",
    description = "By this package, you can simply calculate the epigenetic result caused by a specific disease and reveal the relationship between the epigenetic effect and specific genes' expressions. For numerous samples of a specific disease, you can get a correlation value between gene expression levels and summations calculated from DNA methylation beta-values. Additionally you can simply know beta-value distribution by density plot.",
    long_description = long_description,
    long_description_content_type = "text/markdown",
    url = "https://github.com/JoonHyeongPark/GeneMethyl",
    packages = setuptools.find_packages(),
)
