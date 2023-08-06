import setuptools

with open('README.md', 'r') as file:
    long_description = file.read()

setuptools.setup(
    name="easy_net_tf",
    version="0.0.104",
    author="Ye Hang'yang",
    author_email="yehangyang@qq.com",
    description="A tensorflow-based network utility lib.",
    long_description=long_description,
    long_description_content_type='text/markdown',
    license="MIT",
    url="https://gitlab.espressif.cn:6688/yhy/Network",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: Unix",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
