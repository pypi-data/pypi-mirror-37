from setuptools import setup

setup(name='bilib',
      version='0.1.2',
      description="Bily's personal library",
      author='Bily Lee',
      author_email='bily.lee@qq.com',
      license='MIT',
      packages=['bilib'],
      install_requires=[
        'ipdb',
        'matplotlib',
        'numpy',
        'pillow',
      ],
      zip_safe=False)