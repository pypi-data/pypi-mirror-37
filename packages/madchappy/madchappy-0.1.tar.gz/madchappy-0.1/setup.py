from setuptools import setup

def readme():
    with open('README.md') as f:
        return f.read()

setup(name='madchappy',
      version='0.1',
      description='Private collection of python stuff',
      url='https://gitlab.com/fred.blaise/madchappy',
      author='Fred Blaise',
      author_email='fred.blaise@gmail.com',
      license='MIT',
      packages=['madchappy'],
      install_requires=[
          'requests',
      ],
      zip_safe=False
    )