from setuptools import setup

setup(name='smithclient',
      version='0.1.1',
      description='Monitoring Smith client',
      url='https://github.com/dangavrilin/monitoring_smithclient.git',
      author='Denis Gavrilin',
      author_email='dangavrilin@gmail.com',
      license='MIT',
      packages=['client'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
