# Alpha

## 0.2.22:
 - upgraded to OpenCV 4.0.0-beta
## 0.2.21:
 - updated lange version in classifiers
## 0.2.20:
 - added missing utils module
## 0.2.19:
 - dumped separate release scripts
## 0.2.18:
 - replaced click and crayon with fire and termcolor
 - added black to ensure code style
 - replaced current setup with poetry layout
## 0.2.17:
 - upgraded to OpenCV 4.0.0-alpha
## 0.2.16:
 - upgraded to OpenCV 3.4.3
## 0.2.15:
 - tested against Python 3.7
## 0.2.14:
 - added upload build job
## 0.2.12:
 - upgraded to OpenCV 3.4.2
## 0.2.10:
 - dropped README.rst in favor of markdown
## 0.2.8:
 - upgraded to OpenCV 3.4.1
## 0.2.7:
 - updated README on missing PyPy support
## 0.2.6:
 - added Stopwatch
 - fixed libpython detection on Raspberry Pi
 - added option to override CPU count
## 0.2.5:
 - updated README
 - fixed keep_target_file
## 0.2.4:
 - integrated OpenCV 3.4.0
## 0.2.3:
 - added Raspbian system config
## 0.2.1:
 - fixed Debian config
 - augmented check command -> added test for make and cmake
 - added CLI header
 - creating default temp directory in ~/temp/opencv now in order to preserve sources
## 0.2.0:
 - supported OS: Debian Jessie & Stretch, Ubuntu 16.04, LinuxMint 18.2, Manjaro, Arch
 - added check command
 - integrated click_log
 - replaced click.echo() with standard logger.xxx()
 - implemented safe_command decorator
 - fixed setup.py missing subpackages and data_files
 - restricting minimal Python version
 - added LinuxMint 18.2 config
 - fixed decorator order -> arguments / options
 - fixed Python config dependencies (LinuxMint 18.2, Ubuntu 16.04, possibly for any)
 - added missing Ubuntu config
 - added long description
## 0.1.0:
 - initial release for OpenCV 3.3.1 supporting Manjaro and Debian Jessie
 - CLI interface derived from pipenv
