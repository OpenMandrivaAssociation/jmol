%{?_javapackages_macros:%_javapackages_macros}
%if 0%{?fedora}
%else
Epoch:       1
%global fedora 20
%endif
Name:        jmol
Version:     13.2.4
Release:     1.0%{?dist}
Summary:     An open-source Java viewer for chemical structures in 3D
Group:       Sciences/Chemistry
# most is LGPLv2+, src/com/obrador is combination of IJG and BSD
# src/org@/jmol/export/image is partially 2 clause BSD
License:     LGPLv2+ and IJG and BSD
URL:         https://jmol.sourceforge.net
BuildArch:   noarch
Source0:     http://downloads.sourceforge.net/%{name}/Jmol-%{version}-full.tar.gz
# Image available at "http://wiki.jmol.org:81/index.php/Image:Jmol_icon_128.png"
Source1:     Jmol_icon_128.png
# Patch to get Jmol to build in Fedora (location of JAR files)
Patch0:      jmol-13.2.3-fedorabuild.patch
# Unbundle bundled classes from jars
Patch1:      jmol-13.2.3-unbundle.patch
# Don't try to sign jars
Patch2:      jmol-13.2.3-dontsign.patch
# Don't ignore the system classpath
Patch3:      jmol-12.0.48-classpath.patch


BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:    ant, ant-contrib
BuildRequires:    desktop-file-utils
BuildRequires:    gettext-devel
BuildRequires:    itext
BuildRequires:    apache-commons-cli
BuildRequires:    java-devel >= 1:1.6.0
BuildRequires:    jpackage-utils
BuildRequires:	  jspecview
BuildRequires:	  naga

%if 0%{?fedora} > 14
# In newer releases some of the necessary Java classes are
# in the browser plugin package
BuildRequires:    icedtea-web
Requires:    icedtea-web
%endif

Requires:    java >= 1:1.6.0
Requires:    jpackage-utils
Requires:   itext
Requires:   vecmath
Requires:   apache-commons-cli

%description
Jmol is a free, open source molecule viewer for students, educators,
and researchers in chemistry and biochemistry.


%package javadoc
Summary:    Java docs for %{name}

Requires:    %{name} = %{version}-%{release}
Requires:    jpackage-utils

%description javadoc
This package contains the API documentation for %{name}.


%package doc
Summary:    Documentation for %{name}

Requires:    %{name} = %{version}-%{release}

%description doc
The documentation for %{name}.


%prep
%setup -q
%patch0 -p1 -b .fedorabuild
%patch1 -p1 -b .unbundle
%patch2 -p1 -b .nosign
%patch3 -p1 -b .classpath

# Remove binaries
find -name '*.class' -exec rm -f '{}' \;
find -name '*.exe' -exec rm -f '{}' \;
find -name '*.jar' -exec rm -f '{}' \;
rm -f jars/*

# Remove executable permissions from documentation
find -name "*.txt" -exec chmod 644 {} \;
# Fix EOL encoding
for doc in README.txt COPYRIGHT.txt LICENSE.txt CHANGES.txt; do
sed "s|\r||g" $doc > $doc.new && \
touch -r $doc $doc.new && \
mv $doc.new $doc
done


# Make desktop file
cat > jmol.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=Jmol
Comment=An open-source Java viewer for chemical structures in 3D
Exec=jmol
Icon=jmol
Terminal=false
Type=Application
Categories=Education;Science;Chemistry;Physics;DataVisualization;
EOF

%build
export ANT_OPTS="-Dfile.encoding=utf-8"
%if 0%{?fedora} > 15
# Need to be able to find netscape.javascript.*classes
PLUGIN_JAR=%{_datadir}/icedtea-web/plugin.jar
jar tf $PLUGIN_JAR | grep javascript/JSObject.class
#ant --execdebug -lib $PLUGIN_JAR doc jar applet-jar

ant --execdebug -lib $PLUGIN_JAR jar
ant --execdebug -lib $PLUGIN_JAR applet-jar
ant --execdebug -lib $PLUGIN_JAR doc
%else
ant --execdebug doc jar applet-jar
%endif

%install
rm -rf %{buildroot}
install -D -p -m 644 build/JmolUnsigned.jar %{buildroot}%{_javadir}/Jmol.jar
install -D -p -m 644 build/JmolApplet.jar %{buildroot}%{_javadir}/JmolApplet.jar
install -D -p -m 644 %{SOURCE1} %{buildroot}%{_datadir}/pixmaps/%{name}.png

%jpackage_script org.openscience.jmol.app.Jmol "" "" Jmol:commons-cli:vecmath:itext jmol true

# Install desktop file
desktop-file-install --dir=${RPM_BUILD_ROOT}%{_datadir}/applications \
%if (0%{?fedora} && 0%{?fedora} < 19) || ( 0%{?rhel} && 0%{?rhel} < 7)
--vendor=fedora \
%endif
jmol.desktop

# Javadoc files
mkdir -p %{buildroot}%{_javadocdir}/%{name}
cp -rp build/javadoc/* %{buildroot}%{_javadocdir}/%{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc build/doc/* README.txt COPYRIGHT.txt LICENSE.txt ChangeLog.html CHANGES.txt
%{_bindir}/%{name}
%{_javadir}/Jmol.jar
%{_javadir}/JmolApplet.jar
%{_datadir}/pixmaps/%{name}.png
%if (0%{?fedora} && 0%{?fedora} < 19) || ( 0%{?rhel} && 0%{?rhel} < 7)
%{_datadir}/applications/fedora-%{name}.desktop
%else
%{_datadir}/applications/%{name}.desktop
%endif

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}/

%files doc
%defattr(-,root,root,-)
%doc build/doc/*

%changelog
* Fri Aug 23 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 13.2.4-1
- Update to 13.2.4.

* Sat Aug 10 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 13.2.3-1
- Update to 13.2.3.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 13.0.15-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue May 14 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 13.0.15-1
- Update to 13.0.15.

* Wed Mar  6 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 12.0.48-10
- Remove vendor prefix from desktop files in F19+ https://fedorahosted.org/fesco/ticket/1077

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.48-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Jul 19 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.48-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed May  9 2012 Jussi Lehtola <jussilehtola@fedoraproject.org> - 12.0.48-7
- Remove exe file in %%prep.

* Mon May  7 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 12.0.48-6
- Add forgotten apache-commons BR/R

* Mon May  7 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 12.0.48-5
- Unbundle bundled libraries
- Fix javadoc encoding build problem
- Start using jpackage_script macro
- Fix up license tag somewhat

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 12.0.48-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Aug 24 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 12.0.48-3
- Really fix build by not ignoring system classpath (thanks to omajid).

* Wed Aug 17 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 12.0.48-2
- Try to fix build on rawhide and F16 by adding CLASSPATH definition.

* Wed Aug 17 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 12.0.48-1
- Update to 12.0.48.

* Thu Apr 28 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 12.0.41-1
- Update to 12.0.41.

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.8.26-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Fri Aug 6 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.26-1
- Update to 11.8.26.

* Sat Jul 24 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.25-1
- Update to 11.8.25.

* Tue May 18 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.24-1
- Update to 11.8.24.

* Sun Apr 25 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.23-1
- Update to 11.8.23.

* Fri Mar 26 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.22-1
- Update to 11.8.22.

* Tue Mar 23 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.21-1
- Update to 11.8.21.

* Thu Mar 11 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.20-1
- Update to 11.8.20.

* Fri Mar 05 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.19-1
- Update to 11.8.19.

* Sat Feb 06 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.18-1
- Update to 11.8.18.

* Sat Jan 16 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.17-1
- Update to 11.8.17.

* Thu Jan 14 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.16-1
- Update to 11.8.16.

* Tue Jan 05 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.15-1
- Update to 11.8.15.

* Wed Dec 23 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8.14-1
- Build from stable release tarballs works now, switch to using stable
releases.
- Update to 11.8.14.

* Fri Oct 02 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8-1.11581
- Switch back to tar.bz2 source since xz doesn't work in EL-5.
- Update to svn revision 11581.

* Tue Sep 22 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.8-1.11564
- Update to 11.8 series, svn revision 11564.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.6-12.11223svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-11.11223svn
- Include desktop file in the spec.

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-10.11223svn
- Bump release to be able to rebuild in koji.

* Thu Jul 16 2009 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-9.11223svn
- Update to svn revision 11223.

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 11.6-8.10506svn
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Dec 18 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-7.10506svn
- Remove jpackage-utils from the Requires of the documentation packages.

* Fri Oct 24 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-6.10137svn
- Fix build on EPEL 5.

* Fri Oct 24 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-5.10137svn
- Disable JAR signing.

* Fri Oct 24 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-4.10137svn
- Add gettext-devel to BR and fix desktop-file-install.

* Thu Oct 23 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-3.10137svn
- Update to svn revision 10137.

* Tue Oct 14 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-2.10081svn
- Review fixes.

* Mon Oct 13 2008 Jussi Lehtola <jussilehtola@fedoraproject.org> - 11.6-1.10081svn
- First release.
