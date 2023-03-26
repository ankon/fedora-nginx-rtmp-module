all: build

deps:
	type spectool || dnf install -y rpmdevtools 
	type rpmbuild || dnf install -y rpm-build

fetch:
	spectool -g -R nginx-rtmp-module.spec

build: fetch
	rpmbuild -ba nginx-rtmp-module.spec

