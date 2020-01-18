Name:           nss_wrapper
Version:        1.1.3
Release:        1%{?dist}

License:        BSD
Summary:        A wrapper for the user, group and hosts NSS API
Url:            https://cwrap.org/

Source0:        https://ftp.samba.org/pub/cwrap/%{name}-%{version}.tar.gz

BuildRequires:  cmake
BuildRequires:  libcmocka-devel

Requires:       cmake
Requires:       pkgconfig

%description
There are projects which provide daemons needing to be able to create, modify
and delete Unix users. Or just switch user ids to interact with the system e.g.
a user space file server. To be able to test that you need the privilege to
modify the passwd and groups file. With nss_wrapper it is possible to define
your own passwd and groups file which will be used by software to act correctly
while under test.

If you have a client and server under test they normally use functions to
resolve network names to addresses (dns) or vice versa. The nss_wrappers allow
you to create a hosts file to setup name resolution for the addresses you use
with socket_wrapper.

To use it set the following environment variables:

LD_PRELOAD=libuid_wrapper.so
NSS_WRAPPER_PASSWD=/path/to/passwd
NSS_WRAPPER_GROUP=/path/to/group
NSS_WRAPPER_HOSTS=/path/to/host

This package doesn't have a devel package cause this project is for
development/testing.

%prep
%setup -q

%build
if test ! -e "obj"; then
    mkdir obj
fi
pushd obj
%cmake \
  -DUNIT_TESTING=ON \
  %{_builddir}/%{name}-%{version}

make %{?_smp_mflags} VERBOSE=1
popd

%install
pushd obj
make DESTDIR=%{buildroot} install
popd

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%check
pushd obj
make test
popd

%files
%doc AUTHORS README ChangeLog COPYING
%{_bindir}/nss_wrapper.pl
%{_libdir}/libnss_wrapper.so*
%dir %{_libdir}/cmake/nss_wrapper
%{_libdir}/cmake/nss_wrapper/nss_wrapper-config-version.cmake
%{_libdir}/cmake/nss_wrapper/nss_wrapper-config.cmake
%{_libdir}/pkgconfig/nss_wrapper.pc
%{_mandir}/man1/nss_wrapper.1*

%changelog
* Wed Mar 23 2016 Andreas Schneider <asn@redhat.com> - 1.1.3-1
- Update to version 1.1.3
  * Added support for BSD 'struct passwd' members
  * Replaced strcpy() with snprintf()
  * Fixed segfault while reloading hosts file
  * Fixed issue where are not fault tolerant if an alias has already
    been added
  * Fixed nss_wrapper build on Solaris

* Fri Nov 20 2015 Andreas Schneider <asn@redhat.com> - 1.1.0-1
- Update to version 1.1.0
  * Added support for initgroups()
  * Added support for shadow files (getspnam(), etc.)
  * Improved support for multi address handling in getaddrinfo()
  * Improved file parser
  * Fixed compilation on machines without IPv4 support
  * Fixed service string sanity check in getaddrinfo() (bso #11501)
  * Fixed AI_NUMERICHOST handling in getaddrinfo() (bso #11477)

* Mon Dec 15 2014 Michael Adam <madam@redhat.com> - 1.0.3-2
- Fix format of changelog entries.
- Require cmake.
- Don't own _libdir/pkgconfig, and require pkgconfig instead.

* Thu Sep 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.3-1
- Update to version 1.0.3.

* Wed Apr 09 2014 Andreas Schneider <asn@redhat.com> - 1.0.2-1
- Update to version 1.0.2.

* Fri Mar 14 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-3
- resolves: #1075932 - Fix segfault in 'getent hosts'.

* Tue Feb 11 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-2
- resolves: #1060906 - Fedora package.
- Remove Group
- Remove glibc-devel build requirement
- Do not create a subpackage.

* Tue Feb 04 2014 Andreas Schneider <asn@redhat.com> - 1.0.1-1
- Update to version 1.0.1
  * Added --libs to pkg-config.
  * Added nss_wrapper-config.cmake
  * Fixed a bug packaging the obj directory.

* Mon Feb 03 2014 Andreas Schneider <asn@redhat.com> - 1.0.0-1
- Initial version 1.0.0
