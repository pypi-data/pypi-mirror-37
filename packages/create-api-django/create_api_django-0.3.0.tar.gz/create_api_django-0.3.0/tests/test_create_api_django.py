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


def setup_module():
	cli.create_folder("test_folder")

def teardown_module():
	shutil.rmtree("test_folder")

def test_folder_creation():
	assert os.path.isdir("test_folder")

def test_env_creation():
	cli.create_env("test_folder", 3)
	assert os.path.exists("test_folder/env/bin")
