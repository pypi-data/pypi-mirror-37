# SOMANET Package Installer

Install SOMANET motion drive package to an EtherCAT slave.

## Prerequisite

The Linux OS on which this script is going to be executed must have IgH EtherCAT Master installed and running and slaves have to be powered on. XMOS tools must be added to PATH if you want to erase flash and install bootloader.

## Install

    $ python3 -m pip install somanet-package-installer

## Usage
    usage: somanet-package-installer [-h] [-p position] [-a package] [-e] [-c]
                                    [-s path secret] [-b bin bsp] [-v]

    Install SOMANET motion drive package to an EtherCAT slave.

    optional arguments:
    -h, --help            show this help message and exit
    -p position, --position position
                            slave selection, default is 0.
    -a package, --package package
                            package in zip format.
    -e, --esi             print ESI content to stdout.
    -c, --clear           optionally remove cogging_torque.bin, config.csv and
                            plant_model.csv.
    -s path secret, --stack_info path secret
                            write stack_info.json to slave.
    -b bin bsp, --bootloader bin bsp
                            erase all memory on the flash device and install
                            bootloader.
    -v, --version         show program's version number and exit

## Packaging

### Generating distribution archives

    $ python3 -m pip install --user --upgrade setuptools wheel
    $ python3 setup.py sdist bdist_wheel

### Uploading the distribution archives

    $ python3 -m pip install --user --upgrade twine
    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

### Installing the uploaded package

    $ python3 -m pip install --index-url https://test.pypi.org/simple/ somanet-package-installer
    $ python3 -m pip --no-cache-dir install --index-url https://test.pypi.org/simple/ somanet-package-installer==0.0.8
