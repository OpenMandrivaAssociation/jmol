%define jmoldir	%{_datadir}/%{name}
%define debug_package %{nil}

Name:		jmol
Group:		Sciences/Chemistry
License:	LGPL
Summary:	An open-source Java viewer for chemical structures in 3D
Version:	12.0.22
Release:	2
Source:		http://downloads.sourceforge.net/jmol/Jmol-%{version}-full.tar.gz
URL:		http://www.jmol.org/

Requires:	java > 1.5
BuildRequires:	java-rpmbuild

%description
Jmol: an open-source Java viewer for chemical structures in 3D
with features for chemicals, crystals, materials and biomolecules.

%prep
%setup -q

%build

%install
mkdir -p %{buildroot}%{_datadir}/%{name}
cp -fa *.jar %{buildroot}%{_datadir}/%{name}
cp -far jars appletweb plugin-jars %{buildroot}%{_datadir}/%{name}
cp -fa jmol %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_bindir}
# This is basically a cut&paste of the bundled script, removing
# checks for . directory, and hardcoded /usr/share/jmol
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

# Collect -D & -m options as java arguments
command=java
while [ \`echo \$1 | grep -E '^-D|^-m' | wc -l\` != 0 ]; do
        command="\$command \$1"
        shift
done

if [ x"\$JMOL_HOME" = x ]; then
	JMOL_HOME=%{jmoldir}
fi
jarpath=\$JMOL_HOME/Jmol.jar
if [ ! -f \$jarpath ] ; then
	echo Jmol.jar not found
	exit
fi
\$command -Xmx512m -Djmol.home="\$JMOL_HOME" -jar \$jarpath "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
cp -far doc/* %{buildroot}%{_docdir}/%{name}

%clean

%files
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*


%changelog
* Mon Nov 22 2010 Paulo Andrade <pcpa@mandriva.com.br> 12.0.22-1mdv2011.0
+ Revision: 599831
- Update to latest upstream release

* Tue Oct 26 2010 Paulo Andrade <pcpa@mandriva.com.br> 12.0.19-1mdv2011.0
+ Revision: 589398
- Update to latest upstream release

* Wed Dec 30 2009 Frederik Himpe <fhimpe@mandriva.org> 11.8.15-1mdv2010.1
+ Revision: 483989
- Update to new version 11.8.15

* Mon Oct 26 2009 Paulo Andrade <pcpa@mandriva.com.br> 11.8.6-2mdv2010.0
+ Revision: 459441
- Install "signed" jar files.

* Fri Sep 25 2009 Paulo Andrade <pcpa@mandriva.com.br> 11.8.6-1mdv2010.0
+ Revision: 448539
- update to latest upstream release version 11.8.6.

* Sat May 23 2009 Frederik Himpe <fhimpe@mandriva.org> 11.6.23-1mdv2010.0
+ Revision: 379060
- Update to new version 11.6.23

* Sat May 09 2009 Paulo Andrade <pcpa@mandriva.com.br> 11.6.19-2mdv2010.0
+ Revision: 373566
+ rebuild (emptylog)

* Wed Mar 25 2009 Paulo Andrade <pcpa@mandriva.com.br> 11.6.19-1mdv2009.1
+ Revision: 361185
- Initial import of jmol version 11.6.19.
  Jmol: an open-source Java viewer for chemical structures in 3D
  http://www.jmol.org/
- jmol

