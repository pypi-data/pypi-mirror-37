# -*- coding: utf-8 -*-

"""Console script for create_api_django."""
import click
import os
import sys
import shutil
import subprocess
import tqdm

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def create_folder(path):
	os.makedirs(name=path)

def get_folder_path(path, name):
	if path == "":
		return name
	return (os.path.join(path, name))


def parse_path(path):
	if path == "..":
		cwd = os.getcwd()
		parsed_path = os.path.abspath(os.path.join(cwd, os.pardir))
	elif path == ".":
		parsed_path = os.getcwd()
	return path

def create_env(path, version):
	FNULL = open(os.devnull, 'w')
	print(bcolors.OKGREEN + "Creating virtualenv" + bcolors.ENDC)
	if subprocess.call(["virtualenv", "--python=python" + str(version), os.path.join(path, "env")], stdout=FNULL) != 0:
		print(bcolors.FAIL + "something went wrong while creating a virtualenv. Please check your installation and try again" + bcolors.ENDC)
		sys.exit(1)
	print(bcolors.OKGREEN + "Done" + bcolors.ENDC)
	FNULL.close()


def exec_env(path):
	activate = os.path.join(path, "env", "bin", "activate_this.py")
	if subprocess.call(["python3" ,activate]) != 0:
		print("Something went wrong with your virtualenv activation. Please check your installation and try again")

def install(pip, package):
	FNULL = open(os.devnull, 'w')
	print(bcolors.OKBLUE + "Installing {}".format(package) + bcolors.ENDC)
	if subprocess.call([pip, "install", package], stdout=FNULL, stderr=FNULL) != 0:
		print(bcolors.FAIL + "something went wrong while installing {}".format(package) + bcolors.ENDC)
	FNULL.close()

def install_packages(path, packages):
	activate = os.path.join(path, "env", "bin", "pip")
	print(bcolors.OKGREEN + "Installing packages" + bcolors.ENDC)
	for package in packages:
		install(activate, package)

def init_project(path):
	python_path = os.path.join("env", "bin", "python")
	try:
		subprocess.run(python_path + " " + os.path.join("env", "bin", "django-admin.py") + " startproject api", shell=True, cwd=path)
	except AttributeError:
		subprocess.call([python_path, os.path.join("env", "bin", "django-admin.py"), "startproject api"], shell=True, cwd=path)

@click.command()
@click.argument('name')
@click.option('--path', default="", help="directory of installation")
@click.option('--python', default=3, help='python version for installation. Python 3 is recommended')
@click.option('--verbose', is_flag=True, help='enables complete action log')
def cli(**kwargs):
	path = ""
	packages = [
		"Django",
		"django-allauth",
		"django-cors-headers",
		"django-filter",
		"django-rest-auth",
		"django-rest-framework",
		"django-rest-knox",
		"djangorestframework",
		"djangorestframework-jwt",
		"httpie",
		"mysqlclient",
		"Pillow"]
	if kwargs["path"]:
		path = parse_path(kwargs["path"])
	folder_path = get_folder_path(path, kwargs["name"])
	if os.path.isdir(folder_path):
		r = input("Folder already exists, do you want to overwrite its entirety? [Y/N] ")
		if r == "Y" or r == 'y':
			shutil.rmtree(folder_path)
		else:
			print(bcolors.FAIL + "Please choose another destination for the installation" + bcolors.ENDC)
			sys.exit(1)
	create_folder(folder_path)
	create_env(folder_path, kwargs["python"])
	exec_env(folder_path)
	install_packages(folder_path, packages)
	init_project(folder_path)
	sys.exit(0)

if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
