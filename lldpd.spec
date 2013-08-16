# To build:
#
# You will need the jansson-devel from http://repo.milford.io and the Oracle JDK.
#
# sudo yum -y install rpmdevtools && rpmdev-setuptree
# sudo yum -y install libxml2-devel jansson-devel.
#
# wget https://raw.github.com/nmilford/rpm-lldpd/master/mesos.spec -O ~/rpmbuild/SPECS/mesos.spec
# wget http://media.luffy.cx/files/lldpd/lldpd-0.7.6.tar.gz -O ~/rpmbuild/SOURCES/lldpd-0.7.6.tar.gz
# wget https://raw.github.com/nmilford/rpm-lldpd/master/lldpd.init -O ~/rpmbuild/SOURCES/lldpd.init
# wget https://raw.github.com/nmilford/rpm-lldpd/master/lldpd.sysconfig -O ~/rpmbuild/SOURCES/lldpd.sysconfig
#
# QA_RPATHS=$[ 0x0001|0x0010 ] rpmbuild -bb ~/rpmbuild/SPECS/lldpd.spec

%define lldpd_user _lldpd
%define lldpd_group _lldpd
%define lldpd_chroot /var/run/lldpd

Summary: Implementation of IEEE 802.1ab (LLDP)
Name: lldpd
Version: 0.7.6
Release: 1
License: MIT
Group: System Environment/Daemons
URL: http://vincentbernat.github.com/lldpd/
Source0: http://media.luffy.cx/files/lldpd/%{name}-%{version}.tar.gz
Source1: lldpd.init
Source2: lldpd.sysconfig
BuildRequires: pkgconfig
BuildRequires: readline-devel
BuildRequires: libxml2-devel
BuildRequires: jansson-devel
Requires: libxml2-devel
Requires: jansson-devel
Requires(pre): /usr/sbin/groupadd /usr/sbin/useradd
Requires(post): chkconfig
Requires(preun): chkconfig
Requires(preun): initscripts
Requires(postun): initscripts
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
This implementation provides LLDP sending and reception, supports VLAN
and includes an SNMP subagent that can interface to an SNMP agent
through AgentX protocol.

LLDP is an industry standard protocol designed to supplant proprietary
Link-Layer protocols such as Extreme EDP (Extreme Discovery Protocol)
and CDP (Cisco Discovery Protocol). The goal of LLDP is to provide an
inter-vendor compatible mechanism to deliver Link-Layer notifications
to adjacent network devices.

This daemon is also able to deal with CDP, FDP, SONMP and EDP
protocol. It also handles LLDP-MED extension.

%package devel
Summary:  Implementation of IEEE 802.1ab - Tools and header files for developers
Group:    Development/Libraries
Requires: lldpd = %{version}-%{release}

%description devel
This package is required to develop alternate clients for lldpd.

%prep
%setup -q
%build
%configure \
   --with-xml \
   --enable-cdp \
   --enable-edp \
   --enable-sonmp \
   --enable-fdp \
   --enable-lldpmed \
   --enable-dot1 \
   --enable-dot3 \
   --with-json \
   --with-privsep-user=%lldpd_user \
   --with-privsep-group=%lldpd_group \
   --with-privsep-chroot=%lldpd_chroot \
   --prefix=/usr --localstatedir=%lldpd_chroot --sysconfdir=/etc --libdir=%{_libdir} \
   --docdir=%{_docdir}/lldpd

make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
install -d -m770  $RPM_BUILD_ROOT/%lldpd_chroot
install -d $RPM_BUILD_ROOT/%{_initrddir}
install -m755 %{SOURCE1} $RPM_BUILD_ROOT/%{_initrddir}/lldpd
install -d $RPM_BUILD_ROOT/etc/sysconfig
install -m644 %{SOURCE2} $RPM_BUILD_ROOT/etc/sysconfig/lldpd

%pre
if getent group %lldpd_group >/dev/null 2>&1 ; then : ; else \
 %{_sbindir}/groupadd -r %lldpd_group > /dev/null 2>&1 || exit 1 ; fi
if getent passwd %lldpd_user >/dev/null 2>&1 ; then : ; else \
 %{_sbindir}/useradd -g %lldpd_group -M -r -s /bin/false \
 -c "LLDP daemon" -d %lldpd_chroot %lldpd_user 2> /dev/null \
 || exit 1 ; fi

%post
/sbin/ldconfig
/sbin/chkconfig --add lldpd
%postun
/sbin/ldconfig
if [ "$1" -ge  "1" ]; then
   /sbin/service lldpd condrestart >/dev/null 2>&1 || :
fi
%preun
if [ "$1" = "0" ]; then
   /sbin/service lldpd stop > /dev/null 2>&1
   /sbin/chkconfig --del lldpd
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%dir %{_docdir}/lldpd
%doc %{_docdir}/lldpd/NEWS
%doc %{_docdir}/lldpd/ChangeLog
%doc %{_docdir}/lldpd/README.md
%doc %{_docdir}/lldpd/CONTRIBUTE.md
%{_sbindir}/lldpd
%{_sbindir}/lldpctl
%{_sbindir}/lldpcli
%{_libdir}/liblldpctl.so.*
%doc %{_mandir}/man8/lldp*
%dir %attr(750,root,root) %lldpd_chroot
%config %attr(755,root,root) %{_initrddir}/lldpd
%config(noreplace) /etc/sysconfig/lldpd

%files devel
%defattr(-,root,root)
%{_libdir}/liblldpctl.so
%{_libdir}/liblldpctl.a
%{_libdir}/liblldpctl.la
%{_libdir}/pkgconfig/lldpctl.pc
%{_includedir}/lldpctl.h
%{_includedir}/lldp-const.h

%changelog
* Fri Aug 16 2013 Nathan Milford <nathan@milford.io> - 0.7.6-1
- Builds for CentOS
- Enables JSON and XML output.

* Sat Jun 22 2013 Vincent Bernat <bernat@luffy.cx> - 0.7.5-1
- New upstream version.

* Sun May 12 2013 Vincent Bernat <bernat@luffy.cx> - 0.7.3-1
- New upstream version.

* Fri Apr 19 2013 Vincent Bernat <bernat@luffy.cx> - 0.7.2-1
- New upstream version.

* Sat Jan 12 2013 Vincent Bernat <bernat@luffy.cx> - 0.7.1-1
- New upstream version.

* Sun Jan 06 2013 Vincent Bernat <bernat@luffy.cx> - 0.7.0-1
- New upstream version.
- Requires readline-devel.
- Ships lldpcli.

* Wed Sep 27 2012 Vincent Bernat <bernat@luffy.cx> - 0.6.1-1
- New upstream version
- Do not require libevent, use embedded copy.
- Provide a -devel package.

* Fri Jun 11 2010 Vincent Bernat <bernat@luffy.cx> - 0.5.1-1
- New upstream version
- Define bcond_without and with macros if not defined to be compatible
  with RHEL
- Requires useradd and groupadd
- Adapt to make it work with SuSE
- Provide an init script targetted at SuSE
- Build require lm_sensors-devel on RHEL

* Fri Mar 12 2010 Vincent Bernat <bernat@luffy.cx> - 0.5.0-1
- New upstream version
- Add XML support

* Tue May 19 2009 Vincent Bernat <bernat@luffy.cx> - 0.4.0-1
- Add variables
- Enable SNMP support
- Add _lldpd user creation
- Add initscript
- New upstream version

* Mon May 18 2009 Dean Hamstead <dean.hamstead@optusnet.com.au> - 0.3.3-1
- Initial attempt
