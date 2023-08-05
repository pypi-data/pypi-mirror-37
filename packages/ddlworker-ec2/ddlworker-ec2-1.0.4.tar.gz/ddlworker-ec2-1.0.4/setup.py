import setuptools

version = "1.0.4"
with open("README.md", "r") as fh:
    long_description = fh.read()

    print("Version: {}".format(version))
    setuptools.setup(
        name="ddlworker-ec2",
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
            'cython',
            'pymysql',
            'pyyaml',
            'boto3',
            'urllib3==1.23'
        ],
        classifiers=[
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent",
        ],
    )