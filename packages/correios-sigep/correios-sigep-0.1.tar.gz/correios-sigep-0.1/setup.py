from setuptools import setup

setup(name='correios-sigep',
      version='0.1',
      description='correios sigep',
      url='',
      author='Bruno Casado',
      author_email='contato@brunocasado.me',
      license='MIT',
      packages=['correios_sigep', 'correios_sigep.models', 'correios_sigep.utils', 'correios_sigep.reports'],
      install_requires=[
          'lxml',
          'zeep',
          'elaphe',
          'qrcode',
          'pdfkit',
          'candybar',
          'huBarcode'
      ],
      zip_safe=False)
