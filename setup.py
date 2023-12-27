from setuptools import find_namespace_packages
from setuptools import setup

setup(
    name="skittles",
    version="0.1.1",
    description="mirai-api-http Mock 测试工具",
    long_description=open("README.md", "rt", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RockChinQ/Skittles",
    project_urls={
        "Bug Report": "https://github.com/RockChinQ/Skittles/issues"
    },
    author="RockChinQ",
    author_email="1010553892@qq.com",
    license="GNU Affero General Public License v3.0",
    packages=find_namespace_packages(".", exclude="tests"),
    package_dir={"": "."},
    py_modules=["skittles"],
    package_data={"": ["*.json"]},
    install_requires=[
        "websockets",
        "pydantic",
        "quart",
        "aiocqhttp",
    ],
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Natural Language :: Chinese (Simplified)",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)