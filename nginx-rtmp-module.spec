%global baseversion 1.2.2
%global revision    r1

Name:           nginx-rtmp-module
Version:        %{baseversion}^%{revision}
Release:        1%{?dist}
Summary:        RTMP module for nginx

# BSD License (two clause)
# http://www.freebsd.org/copyright/freebsd-license.html
License:        BSD
URL:            https://github.com/sergey-dryabzhinsky/nginx-rtmp-module
Source0:        https://github.com/sergey-dryabzhinsky/nginx-rtmp-module/archive/refs/tags/v%{baseversion}-%{revision}.tar.gz

BuildRequires:  nginx-mod-devel

%nginx_modrequires

%description


%prep
%autosetup -n %{name}-%{baseversion}-%{revision}


%conf
%nginx_modconfigure

%build
%nginx_modbuild


%install
install -p -d -m 0755 %{buildroot}%{nginx_modconfdir}
install -p -d -m 0755 %{buildroot}%{nginx_moddir}
install -p -d -m 0755 %{buildroot}%{_datadir}/nginx/rtmp
install -p -m 0755 %{_vpath_builddir}/ngx_rtmp_module.so %{buildroot}%{nginx_moddir}
install -p -m 0644 stat.xsl %{buildroot}%{_datadir}/nginx/rtmp

echo 'load_module "%{nginx_moddir}/ngx_rtmp_module.so";' \
    > %{buildroot}%{nginx_modconfdir}/mod-rtmp.conf

%post
%systemd_post nginx.service

if [ $1 -eq 1 ]; then
    /usr/bin/systemctl reload nginx.service >/dev/null 2>&1 || :
fi

%preun
%systemd_preun nginx.service

%postun
%systemd_postun nginx.service
if [ $1 -ge 1 ]; then
    /usr/bin/nginx-upgrade >/dev/null 2>&1 || :
fi


%files
%license LICENSE
%doc doc/*.md
%{nginx_modconfdir}/mod-rtmp.conf
%{nginx_moddir}/ngx_rtmp_module.so
%{_datadir}/nginx/rtmp/stat.xsl

%changelog
* Sun Mar 26 2023 Andreas Kohn <andreas.kohn@gmail.com>
- 
