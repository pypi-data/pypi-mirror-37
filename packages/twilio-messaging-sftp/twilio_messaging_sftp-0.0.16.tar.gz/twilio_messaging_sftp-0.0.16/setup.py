import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="twilio_messaging_sftp",
    version="0.0.16",
    author="messaging sftp",
    author_email="ebogod@twilio.com",
    description="Library for sending bulk sms/mms messages via sftp",
    long_description=long_description,
    url="https://code.hq.twilio.com/messaging/messaging-sftp-lib",
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    include_package_data=True,
    install_requires=[
        'twilio==6.19.2',
        'boto3==1.9.35'
    ]
)
