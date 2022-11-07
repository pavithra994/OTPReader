from setuptools import setup

setup(
    name='Bank OTP Scrapper',
    version='0.1.0',
    description='this program will scrap out OTPs from your gmail account',
    url='https://github.com/pavithra994/OTPReader',
    author='Pavithra Weerapperuma',
    author_email='pavithra.blog@gmail.com',
    license='BSD 2-clause',
    packages=['bank_otp_scrapper'],
    install_requires=["google-api-python-client",
                      "google-auth-httplib2",
                      "google-auth-oauthlib"
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: MIT',
        'Programming Language :: Python :: 3',
    ],
)