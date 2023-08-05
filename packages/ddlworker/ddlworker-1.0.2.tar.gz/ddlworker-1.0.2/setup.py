import setuptools

version = "1.0.2"
with open("README.md", "r") as fh:
    long_description = fh.read()

    print("Version: {}".format(version))
    setuptools.setup(
        name="ddlworker",
        version=version,
        author="YL & SW",
        author_email = 'nedlitex0053@gmail.com',
        description="cli for distributed deep learning worker",
        long_description=long_description,
        long_description_content_type="text/markdown",
        packages=setuptools.find_packages(),
        entry_points={
            'console_scripts': [
                'ddlworker=main.worker_main:main',
            ],
        },
        install_requires=[
            'requests',
            'tensorflow>=1.9.0,<2.0',
            'tensorflow-gpu>=1.9.0,<2.0',
            'cython',
            'pymysql',
            'pyyaml',
            'boto3'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    )