#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os
import glob
import shutil


def install_file(source_filename, dest_filename):
    # do not overwrite network configuration if it exists already
    # https://github.com/wocsa/cleanagotchi/issues/483
    if dest_filename.startswith('/etc/network/interfaces.d/') and os.path.exists(dest_filename):
        print("%s exists, skipping ..." % dest_filename)
        return

    print("installing %s to %s ..." % (source_filename, dest_filename))
    try:
        dest_folder = os.path.dirname(dest_filename)
        if not os.path.isdir(dest_folder):
            os.makedirs(dest_folder)

        shutil.copyfile(source_filename, dest_filename)
    except Exception as e:
        print("error installing %s: %s" % (source_filename, e))


def install_system_files():
    setup_path = os.path.dirname(__file__)
    data_path = os.path.join(setup_path, "builder/data")

    for source_filename in glob.glob("%s/**" % data_path, recursive=True):
        if os.path.isfile(source_filename):
            dest_filename = source_filename.replace(data_path, '')
            install_file(source_filename, dest_filename)

    # reload systemd units
    os.system("systemctl daemon-reload")


install_system_files()

required = []
with open('requirements.txt') as fp:
    for line in fp:
        line = line.strip()
        if line != "":
            required.append(line)

import cleanagotchi

setup(name='cleanagotchi',
      version=cleanagotchi.version,
      description='(⌐■_■) - Deep Reinforcement Learning instrumenting bettercap for WiFI pwning.',
      author='evilsocket && the dev team',
      author_email='evilsocket@gmail.com',
      url='https://cleanagotchi.ai/',
      license='GPL',
      install_requires=required,
      scripts=['bin/cleanagotchi'],
      package_data={'cleanagotchi': ['defaults.yml', 'cleanagotchi/defaults.yml', 'locale/*/LC_MESSAGES/*.mo']},
      include_package_data=True,
      packages=find_packages(),
      classifiers=[
          'Programming Language :: Python :: 3',
          'Development Status :: 5 - Production/Stable',
          'License :: OSI Approved :: GNU General Public License (GPL)',
          'Environment :: Console',
      ])
