import pip
import os
import inspect

def install(package):
    print(package)
    pip.main(['install', package])

requirements = [
    'selenium',
    'lxml',
    'requests',
    'shutil',
    'urllib',
    'pdfx',
    'tkinter'
]

# Example
if __name__ == '__main__':
	for package in requirements:
		install(package)
		