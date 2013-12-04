%define jmoldir	%{_datadir}/%{name}
%define debug_package %{nil}

Name:		jmol
Group:		Sciences/Chemistry
License:	LGPL
Summary:	An open-source Java viewer for chemical structures in 3D
Version:	13.2.7
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
mkdir -p %{buildroot}%{_javadir} %{buildroot}%{jmoldir}
cp -fa *.jar %{buildroot}%{_javadir}
cp -far jars appletweb plugin-jars %{buildroot}%{jmoldir}
cp -fa jmol %{buildroot}%{jmoldir}

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
	JMOL_HOME=%{_javadir}
fi
jarpath=%{_javadir}/Jmol.jar
if [ ! -f \$jarpath ]; then
	echo Jmol.jar not found
	exit
fi
\$command -Xmx512m -Djmol.home="\$JMOL_HOME" -jar \$jarpath "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{_docdir}/%{name}
cp -far doc/* %{buildroot}%{_docdir}/%{name}

%files
%{_bindir}/%{name}
%{_javadir}/*.jar
%{jmoldir}
%doc %{_docdir}/%{name}
