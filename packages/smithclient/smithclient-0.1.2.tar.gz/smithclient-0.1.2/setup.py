from setuptools import setup

setup(name='smithclient',
      version='0.1.2',
      description='Monitoring Smith smithclient',
      url='https://github.com/dangavrilin/monitoring_smithclient.git',
      author='Denis Gavrilin',
      author_email='dangavrilin@gmail.com',
      license='MIT',
      packages=['smithclient'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
