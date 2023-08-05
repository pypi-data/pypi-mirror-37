%global srcname  ligo-segments

Name:           %{srcname}
Version:        1.1.0
Release:        1%{?dist}
Summary:        Representations of semi-open intervals

License:        GPLv3
URL:            https://git.ligo.org/lscsoft/ligo-segments/
Source0:        https://files.pythonhosted.org/packages/source/p/%{srcname}/%{srcname}-%{version}.tar.gz

BuildRequires:  python3-rpm-macros
BuildRequires:  python-devel
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python2-setuptools
BuildRequires:  python%{python3_pkgversion}-setuptools
BuildRequires:  python-six
BuildRequires:  python%{python3_pkgversion}-six
BuildRequires:  pytest
BuildRequires:  python%{python3_pkgversion}-pytest

%description
This module defines the segment and segmentlist objects, as well as the
infinity object used to define semi-infinite and infinite segments.

%package -n python2-%{srcname}
Summary:  %{summary}
Requires: python-six
Requires: ligo-common
Recommends: python2-lal

%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
This module defines the segment and segmentlist objects, as well as the
infinity object used to define semi-infinite and infinite segments.

%package -n python%{python3_pkgversion}-%{srcname}
Summary:  %{summary}
Requires: python%{python3_pkgversion}-six
Requires: python%{python3_pkgversion}-ligo-common
Recommends: python3-lal

%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}

%description -n python%{python3_pkgversion}-%{srcname}
This module defines the segment and segmentlist objects, as well as the
infinity object used to define semi-infinite and infinite segments.

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
cd test
# hack the python site to read from the build path:
echo "import site; site.addsitedir('$RPM_BUILD_ROOT%{python2_sitearch}')" > $RPM_BUILD_ROOT%{python2_sitearch}/sitecustomize.py
echo "import site; site.addsitedir('$RPM_BUILD_ROOT%{python3_sitearch}')" > $RPM_BUILD_ROOT%{python3_sitearch}/sitecustomize.py
# run the tests
make check PYTHON=%{__python2} PYTHONPATH="$RPM_BUILD_ROOT%{python2_sitearch}"
make check PYTHON=%{__python3} PYTHONPATH="$RPM_BUILD_ROOT%{python3_sitearch}"
# clean up the sitecustomize hack
rm -v \
    $RPM_BUILD_ROOT%{python2_sitearch}/sitecustomize.py* \
    $RPM_BUILD_ROOT%{python3_sitearch}/sitecustomize.py* \
    $RPM_BUILD_ROOT%{python3_sitearch}/__pycache__/sitecustomize.*.pyc
rm -vd $RPM_BUILD_ROOT%{python3_sitearch}/__pycache__/

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitearch}/*

%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitearch}/*

%changelog
* Thu May 10 2018 Duncan Macleod <duncan.macleod@ligo.org>
- 1.0.0: first release of ligo.segments, should be funtionally identical to glue.segments
