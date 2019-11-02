#!/bin/bash

rm -rf build dist cleanagotchi.egg-info &&
  python3 setup.py sdist bdist_wheel &&
  clear &&
  twine upload dist/*
