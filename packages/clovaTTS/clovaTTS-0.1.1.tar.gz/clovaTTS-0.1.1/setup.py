from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(name='clovaTTS',
      version='0.1.1',
      description='A TTS Wrapper for Naver Clova Speech Synthesis API',
      long_description=long_description,
      long_description_content_type="text/markdown",
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
      ],
      keywords='tts naver clova',
      url='https://github.com/zebehn/clovaTTS',
      author='Minsu Jang',
      author_email='minsu@etri.re.kr',
      license='MIT',
      packages=['clovaTTS'],
      install_requires=[
      ],
      include_package_data=True,
      zip_safe=False)