Name:           buildnumber-maven-plugin
Version:        1.0
Release:        4
Summary:        Build Number Maven Plugin

Group:          Development/Java
License:        MIT
# svn export http://svn.codehaus.org/mojo/tags/buildnumber-maven-plugin-1.0 buildnumber-maven-plugin
URL:            http://svn.codehaus.org/mojo/tags/buildnumber-maven-plugin-1.0

# tar caf buildnumber-maven-plugin-1.0.tar.xz buildnumber-maven-plugin
Source0:        buildnumber-maven-plugin-1.0.tar.xz
Source1:	%{name}-depmap.xml

Patch0:  	0001-Add-source-and-target-version-for-compiler.patch
Patch1:		0002-Remove-maven-scm-provider-svnjava-dependency.patch

BuildArch: 	noarch

# Basic stuff
BuildRequires: jpackage-utils
BuildRequires: java-devel >= 0:1.6.0

# Maven and its dependencies
BuildRequires: maven
BuildRequires: maven2-common-poms
BuildRequires: maven-plugin-plugin
BuildRequires: maven-idea-plugin
BuildRequires: maven-resources-plugin
BuildRequires: maven-compiler-plugin
BuildRequires: maven-install-plugin
BuildRequires: maven-javadoc-plugin
BuildRequires: maven-jar-plugin
BuildRequires: maven-enforcer-plugin
BuildRequires: maven-invoker-plugin
BuildRequires: maven-doxia
BuildRequires: maven-doxia-tools
BuildRequires: maven-doxia-sitetools
BuildRequires: maven-surefire-provider-junit
BuildRequires: maven-surefire-plugin
BuildRequires: maven-plugin-cobertura
BuildRequires: plexus-containers-component-javadoc
BuildRequires: svnkit
BuildRequires: jna
BuildRequires: mojo-parent

Requires: java
Requires: maven
Requires: jna
Requires: svnkit
Requires: jpackage-utils
Requires: mojo-parent
Requires(post): jpackage-utils
Requires(postun): jpackage-utils

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
Group:          Development/Java
Summary:        Javadoc for %{name}
Requires:       jpackage-utils

%description javadoc
API documentation for %{name}.

%prep
%setup -q -n %{name}

%patch0 -p1
%patch1 -p1

%build

# tests skipped due to invoker problems with local repository tests
mvn-rpmbuild -DskipTests=true \
        -Dmaven.local.depmap.file=%{SOURCE1} \
        -Dmaven.test.skip=true \
        install javadoc:javadoc

%install

# jars
install -d -m 0755 %{buildroot}%{_javadir}
install -m 644 target/%{name}-%{version}.jar   %{buildroot}%{_javadir}/%{name}.jar

%add_to_maven_depmap org.codehaus.mojo buildnumber-maven-plugin %{version} JPP buildnumber-maven-plugin

# poms
install -d -m 755 %{buildroot}%{_mavenpomdir}
install -pm 644 pom.xml \
    %{buildroot}%{_mavenpomdir}/JPP-%{name}.pom

# javadoc
install -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
cp -pr target/site/api*/* %{buildroot}%{_javadocdir}/%{name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%doc LICENSE.txt
%{_javadir}/*
%{_mavenpomdir}/*
%{_mavendepmapfragdir}/*

%files javadoc
%doc LICENSE.txt
%{_javadocdir}/%{name}

