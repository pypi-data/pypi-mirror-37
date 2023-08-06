from distutils.core import setup
from distutils.command.install_scripts import install_scripts
import os

exec(open('version.py').read())
version = __version__  # noqa


class verisk_install_scripts(install_scripts):
    def run(self):
        install_scripts.run(self)
        os.system('verisk -m')  # generate the initial verisk ID


setup(name="verisk",
      version=version,
      description="Simple persistent unique IDs.",
      author="Taewon Kang",
      author_email="tkang007@gmail.com",
      url="https://github.com/tkang007/verisk/",
      license='bsd',
      py_modules=['verisk'],
      scripts=['verisk'],
      cmdclass={"install_scripts": verisk_install_scripts},
      classifiers=[
          'Operating System :: POSIX',
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: BSD License',
          'Programming Language :: Python :: 2.7',
          'Programming Language :: Python :: 3',
          'Topic :: Software Development :: Libraries',
          'Topic :: Utilities', ],
      keywords='unique id uuid persistent identification',
      )
