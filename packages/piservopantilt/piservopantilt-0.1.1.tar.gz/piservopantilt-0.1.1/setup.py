#!/usr/bin/env python3

import setuptools

with open("README.md", "r") as f:
	long_description = f.read()

setuptools.setup(
	name="piservopantilt",
	version="0.1.1",
	author="Toni Kangas",
	description="Scripts to control servos in pan-tilt configuration with Raspberry Pi",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url="https://github.com/kangasta/piservopantilt",
	packages=setuptools.find_packages(),
	scripts=["bin/piservo"],
	install_requires=[
		"pigpio",
		"resettabletimer"
	],
	classifiers=(
		"Programming Language :: Python :: 2.7",
		"Programming Language :: Python :: 3",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	)
)