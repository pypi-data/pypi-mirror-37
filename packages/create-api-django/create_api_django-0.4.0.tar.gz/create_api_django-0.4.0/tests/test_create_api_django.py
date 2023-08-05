#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `create_api_django` package."""

import pytest

from click.testing import CliRunner

from create_api_django import create_api_django
from create_api_django import cli
import os
import sys
import shutil
import re


def setup_module():
	cli.create_folder("test_folder")

def teardown_module():
	shutil.rmtree("test_folder")

def test_folder_creation():
	assert os.path.isdir("test_folder")

def test_env_creation():
	cli.create_env("test_folder", 3)
	assert os.path.exists("test_folder/env/bin")

def test_package_install():
	cli.install("test_folder/env/bin/pip", "django")
	lib_dir = os.listdir("test_folder/env/lib")
	for item in lib_dir:
		if item.startswith('python'):
			assert os.path.isdir(os.path.join("test_folder/env/lib", item, "site-packages", "django"))

def test_project_init():
	cli.init_project("test_folder")
	assert os.path.isdir(os.path.join("test_folder", "api"))