rpm-lldpd
=========

An RPM spec file to build and install lldpd with XML and JSON output enabled.

snmp support is disabled, because perl.

To build:

You will need the `jansson-devel` from http://repo.milford.io and the Oracle JDK.

`sudo yum -y install rpmdevtools && rpmdev-setuptree`

`sudo yum -y install libxml2-devel jansson-devel`

`wget https://raw.github.com/nmilford/rpm-lldpd/master/mesos.spec -O ~/rpmbuild/SPECS/mesos.spec`

`wget http://media.luffy.cx/files/lldpd/lldpd-0.7.6.tar.gz -O ~/rpmbuild/SOURCES/lldpd-0.7.6.tar.gz`

`wget https://raw.github.com/nmilford/rpm-lldpd/master/lldpd.init -O ~/rpmbuild/SOURCES/lldpd.init`

`wget https://raw.github.com/nmilford/rpm-lldpd/master/lldpd.sysconfig -O ~/rpmbuild/SOURCES/lldpd.sysconfig`

`QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/lldpd.spec`