%define pypi_name neutron-bsn-lldp
%define pypi_name_underscore neutron_bsn_lldp

Name:               %{pypi_name}
Version:            1.0.0
Release:            1%{?dist}
Epoch:              1
Summary:            LLDP Agent for Big Switch Networks integration.
License:            ASL 2.0
URL:                https://pypi.python.org/pypi/%{pypi_name}
Source0:            https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
Source1:            neutron-bsn-lldp.service
BuildArch:          noarch

BuildRequires:      python-pbr
BuildRequires:      python-setuptools

Requires:           python-pbr >= 0.10.8
Requires:           python-oslo-serialization >= 2.20.2
Requires:           os-net-config >= 7.3.6

Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

%description
===============================
neutron-bsn-lldp
===============================

LLDP Agent for Big Switch Networks integration.

This custom LLDP agent is used to send LLDPs on interfaces connected to
Big Cloud Fabric (BCF). In environments with os-net-config installed, it reads
config from os-net-config to automagically identify and send LLDPs.

For all other purposes, Big Switch Openstack Installer (BOSI) configures the
service file based on environment info.


%prep
%setup -q -n %{pypi_name}-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}
install -p -D -m 644 %{SOURCE1} %{buildroot}%{_unitdir}/neutron-bsn-lldp.service

%clean
rm -rf $RPM_BUILD_ROOT

%files
%license LICENSE
%{python2_sitelib}/%{pypi_name_underscore}
%{python2_sitelib}/*.egg-info
%{_unitdir}/neutron-bsn-lldp.service
%{_bindir}/bsnlldp

%post
%systemd_post neutron-bsn-lldp.service

%preun
%systemd_preun neutron-bsn-lldp.service

%postun
%systemd_postun_with_restart neutron-bsn-lldp.service

%changelog
* Tue Oct 09 2018 Aditya Vaja <wolverine.av@gmail.com> - 1.0.0
- first stable release
* Tue Aug 28 2018 Aditya Vaja <wolverine.av@gmail.com> - 0.0.1
- initial commit for neutron-bsn-lldp
