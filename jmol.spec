%define name	jmol
%define jmoldir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Chemistry
License:	LGPL
Summary:	Jmol: an open-source Java viewer for chemical structures in 3D
Version:	11.6.19
Release:	%mkrel 1
Source:		http://downloads.sourceforge.net/jmol/jmol-11.6.19-full.tar.gz
URL:		http://www.jmol.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

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
cp -fa `ls *.jar | grep -v Signed` %{buildroot}%{_datadir}/%{name}
cp -far jars appletweb plugin-jars %{buildroot}%{_datadir}/%{name}
cp -fa jmol %{buildroot}%{_datadir}/%{name}

mkdir -p %{buildroot}%{_bindir}
# This is basically a cut&paste of the bundled script, removing
# checks for . directory, and hardcoded /usr/share/jmol
cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

# Collect -D & -m options as java arguments
command=java
while [ \`echo \$1 | egrep '^-D|^-m' | wc -l\` != 0 ]; do
        command="\$command \$1"
        shift
done

if [ -f \$JMOL_HOME/Jmol.jar ] ; then
  jarpath=\$JMOL_HOME/Jmol.jar
elif [ -f %{jmoldir}/Jmol.jar ] ; then
  jarpath=%{jmoldir}/Jmol.jar
else
  echo Jmol.jar not found
  exit
fi
\$command -Xmx512m -jar \$jarpath \$@
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
cp -far doc/* %{buildroot}%{_docdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/*
%dir %doc %{_docdir}/%{name}
%doc %{_docdir}/%{name}/*
