%global pypi_name python-bsn-neutronclient
%global pypi_name_underscore python_bsn_neutronclient
%global rpm_prefix openstackclient-bigswitch

Name:           %{pypi_name}
Version:        0.0.5
Release:        1%{?dist}
Epoch:          1
Summary:        Python bindings for Big Switch Networks Neutron API
License:        ASL 2.0
URL:            https://pypi.python.org/pypi/%{pypi_name}
Source0:        https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python-pbr
BuildRequires:  python-setuptools

Requires:       python-pbr >= 0.10.8
Requires:       python-neutronclient >= 6.3.0

%description
This package contains Big Switch Networks
python client for Openstack CLI.

%prep
%setup -q -n %{pypi_name}-%{version}

%build
export PBR_VERSION=%{version}
export SKIP_PIP_INSTALL=1
%{__python2} setup.py build

%install
%{__python2} setup.py install --skip-build --root %{buildroot}

%files
%license LICENSE
%{python2_sitelib}/%{pypi_name_underscore}
%{python2_sitelib}/*.egg-info


%post

%preun

%postun

%changelog
* Mon Oct 08 2018 Aditya Vaja <wolverine.av@gmail.com> - 0.0.5
- OSP-241: fix entry point extension name and import error
* Tue Aug 21 2018 Aditya Vaja <wolverine.av@gmail.com> - 0.0.4
- OSP-165: add force sync command for topo_sync and build changes
