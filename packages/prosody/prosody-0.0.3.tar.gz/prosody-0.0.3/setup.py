import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='prosody',
    version='0.0.3',
    author='Suwon Shin, Yuneui Jeong',
    author_email='ssw0093@humelo.com, yjeong@humelo.com',
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
