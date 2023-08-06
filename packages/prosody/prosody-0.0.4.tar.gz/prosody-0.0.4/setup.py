import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='prosody',
    version='0.0.4',
    author='Yuneui Jeong, Suwon Shin',
    author_email='yjeong@humelo.com, ssw0093@humelo.com',
    description='Python Prosody API: Emotion & Prosody sensitive TTS',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=['prosody'],
    install_requires=[
        'aiodns',
        'aiohttp',
        'cchardet',
        'requests'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
