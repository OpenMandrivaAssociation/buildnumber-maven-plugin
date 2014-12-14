%{?_javapackages_macros:%_javapackages_macros}
Name:           buildnumber-maven-plugin
Version:        1.3
Release:        1.1
Summary:        Build Number Maven Plugin

Group:          System/Libraries
License:        MIT and ASL 2.0
URL:            http://svn.codehaus.org/mojo/tags/buildnumber-maven-plugin-%{version}

Source0:        http://central.maven.org/maven2/org/codehaus/mojo/%{name}/%{version}/%{name}-%{version}-source-release.zip
Source1:        http://www.apache.org/licenses/LICENSE-2.0.txt

BuildArch: 	noarch

# Basic stuff
BuildRequires: jpackage-utils
BuildRequires: java-devel >= 1:1.6.0

# Maven and its dependencies
BuildRequires: maven-local
BuildRequires: cobertura-maven-plugin
BuildRequires: jna
BuildRequires: maven-scm

Requires: java-headless
Requires: maven
Requires: maven-project
Requires: maven-scm
Requires: jna
Requires: jpackage-utils
Requires: mojo-parent
Requires: plexus-containers-container-default
Requires: plexus-utils

%description
This mojo is designed to get a unique build number for each time you build
your project. So while your version may remain constant at 1.0-SNAPSHOT
for many iterations until release, you will have a build number that can
uniquely identify each build during that time. The build number is obtained
from scm, and in particular, at this time, from svn. You can then place that
build number in metadata, which can be accessed from your app, if desired.

The mojo also has a couple of extra functions to ensure you get the proper
build number. First, your local repository is checked to make sure it is
up to date. Second, your local repository is automatically updated, so that
you get the latest build number. Both these functions can be suppressed,
if desired.

Optionally, you can configure this mojo to produce a revision based on a
timestamp, or on a sequence, without requiring any interaction with an
SCM system. Note that currently, the only supported SCM is subversion.


%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q
cp -p %{SOURCE1} .

%pom_remove_dep com.google.code.maven-scm-provider-svnjava:maven-scm-provider-svnjava
%pom_remove_dep org.tmatesoft.svnkit:svnkit
%pom_remove_plugin :maven-enforcer-plugin
%pom_remove_plugin :maven-invoker-plugin

%build
%mvn_build

%install
%mvn_install

%files -f .mfiles
%doc LICENSE.txt LICENSE-2.0.txt

%files javadoc -f .mfiles-javadoc
%doc LICENSE.txt LICENSE-2.0.txt

%changelog
* Fri Jun 13 2014 Alexander Kurtakov <akurtako@redhat.com> 1.3-1
- Update to upstream 1.3 release.

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 04 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.2-7
- Use Requires: java-headless rebuild (#1067528)

* Sat Aug 24 2013 Mat Booth <fedora@matbooth.co.uk> - 1.2-6
- Remove unneeded BR on maven2-common-poms

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Mon Apr 29 2013 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.2-4
- Remove unneeded BR: maven-idea-plugin

* Thu Feb 28 2013 Weinan Li <weli@redhat.com> - 1.2-3
- remove unnecessary maven-doxia dependencies

* Wed Feb 06 2013 Java SIG <java-devel@lists.fedoraproject.org> - 1.2-2
- Update for https://fedoraproject.org/wiki/Fedora_19_Maven_Rebuild
- Replace maven BuildRequires with maven-local

* Tue Jan 29 2013 David Xie <david.scriptfan@gmail.com> - 1.2-1
- Upgrade to 1.2

* Thu Aug 16 2012 Mikolaj Izdebski <mizdebsk@redhat.com> - 1.1-2
- Install ASL 2.0 license
- Remove rpm bug workaround

* Wed Jul 25 2012 Tomas Radej <tradej@redhat.com> - 1.1-1
- Updated to latest upstream version
- Replaced patches with pom macros

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Feb 10 2012 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-5
- Remove dependency on svnkit

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Thu Jun 30 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-3
- Add missing (Build)Requires
- Use new add_maven_depmap macro

* Wed Jun 8 2011 Alexander Kurtakov <akurtako@redhat.com> 1.0-2
- Do not require maven2.
- Guidelines fixes.

* Mon Apr 18 2011 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-1
- Update to latest upstream
- Build with maven 3
- Tweaks according to new guidelines
- Versionless jars & javadocs

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.11.b4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Thu Nov 11 2010 Stanislav Ochotnicky <sochotnicky@redhat.com> - 1.0-0.10.b4
- Added mojo-parent to BR/R

* Wed Sep 1 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.9.b4
- Fix build and use new maven plugins names.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.8.b4
- BR maven2-common-poms.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.7.b4
- Disable it-tests and changes plugin.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.6.b4
- Skip tests to be able to rebuild.

* Thu Jun 17 2010 Alexander Kurtakov <akurtako@redhat.com> 1.0-0.5.b4
- Add missing requires.

* Thu May 27 2010 Weinan Li <weli@redhat.com> - 1.0-0.4.b4
- License.txt and Readme.txt added as %doc

* Thu May 27 2010 Weinan Li <weli@redhat.com> - 1.0-0.3.b4
- Fix javadoc dangling-relative-symlink

* Wed May 26 2010 Weinan Li <weli@redhat.com> - 1.0-0.2.b4
- Add requires on jpackage-utils for javadoc subpackage
- Add standard jpackage-utils requires on main package
- Use global instead of define
- Fix license to MIT
- fix incoherent-version-in-changelog

* Mon May 24 2010 Weinan Li <weli@redhat.com> - 1.0-0.1.b4
- Initial package

