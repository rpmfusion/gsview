%global tag v5.01beta
%global libgspath %{_libdir}/libgs.so.{?,??}

Summary: PostScript and PDF previewer
Name: 	 gsview
Version: 5.01~beta
Release: 8%{?dist}

License: GPLv3
Group: 	 Applications/Publishing
URL: 	 http://www.ghostgum.com.au/
# wget --content-disposition "https://git.ghostscript.com/?p=user/ghostgum/gsview.git;a=snapshot;h=refs/tags/v5.01beta;sf=tgz"
Source0: gsview-v5.01beta.tar.gz
Source1: gsview.desktop

BuildRequires: gcc
BuildRequires: gtk+-devel
BuildRequires: desktop-file-utils
BuildRequires: sed >= 4.0
BuildRequires: ghostscript-devel >= 7.07-15.3
# Needed because ghostscript-devel has been replaced by libgs-devel in f28
BuildRequires: ghostscript
%global gs_ver  %(gs --version 2> /dev/null | cut -d. -f-2 )

Requires: ghostscript >= 7.07-15.3
Requires: xdg-utils

## Use xdg-open instead of hard-coded mozilla
Patch1: gsview-4.4-xdg_open.patch
# default to libgs.so.@@SOMAJOR@@ instead of libgs.so
Patch2: gsview-4.8-libgs.patch
# attempt to allow/use ghostscript-8.15 reported value of 81500.
# http://bugzilla.redhat.com/159912
Patch3: gsview-4.7-dllversion.patch
# Change Paper default A4 -> Letter
Patch4: gsview-4.7-letterpaper.patch
Patch5: 0001-Updates-for-registraton-removal-in-the-unix-specific.patch

%description
GSview is a graphical interface for Ghostscript.
Ghostscript is an interpreter for the PostScript page
description language used by laser printers.
For documents following the Adobe PostScript Document Structuring
Conventions, GSview allows selected pages to be viewed or printed.

%prep
%autosetup -n %{name}-%{tag} -p1

GS_REVISION=%(echo %{gs_ver} | tr -d '.' )
sed -i -e "s|@@GS_REVISION@@|${GS_REVISION}|g" src/gvcver.h

# Sanity check to make sure libgs.so exists
libgs=$(ls %{libgspath} 2>/dev/null || true)
if [ -f "$libgs" ]; then
  echo Found ${libgs}. Proceeding...
else
  echo Error: %{libgspath} not found. Aborting...
  exit 1
fi

SOMAJOR=$(basename %{libgspath} | sed -e 's@libgs.so.@@' )
sed -i -e "s|@@SOMAJOR@@|${SOMAJOR}|g" src/gvcver.h

%build
make -f srcunx/unx.mak \
  RPM_OPT_FLAGS="%{!?debug_package:-g0} $RPM_OPT_FLAGS" \
  GSVIEW_BASE=%{_prefix} \
  GSVIEW_BINDIR=%{_bindir} \
  GSVIEW_MANDIR=%{_mandir} \
  GSVIEW_DOCPATH=%{_docdir} \
  GSVIEW_ETCPATH=%{_sysconfdir}

%install
install -d $RPM_BUILD_ROOT{%{_bindir},%{_mandir},%{_docdir},%{_sysconfdir}}

make -f srcunx/unx.mak install \
  GSVIEW_BASE=$RPM_BUILD_ROOT%{_prefix} \
  GSVIEW_BINDIR=$RPM_BUILD_ROOT%{_bindir} \
  GSVIEW_MANDIR=$RPM_BUILD_ROOT%{_mandir} \
  GSVIEW_DOCPATH=$RPM_BUILD_ROOT%{_docdir} \
  GSVIEW_ETCPATH=$RPM_BUILD_ROOT%{_sysconfdir}

# desktop/icon files
install -D -p -m644 binary/gsview48.png\
  $RPM_BUILD_ROOT%{_datadir}/icons/hicolor/48x48/apps/gsview.png

desktop-file-install \
  --dir="$RPM_BUILD_ROOT%{_datadir}/applications" \
  --vendor="" \
  %{SOURCE1}

%files
%doc %{_docdir}/*
%{_bindir}/*
%dir %{_sysconfdir}/gsview
%config(noreplace) %{_sysconfdir}/gsview/printer.ini
%{_mandir}/man*/*
%{_datadir}/applications/*.desktop
%{_datadir}/icons/hicolor/*/*/*

%changelog
* Wed Jan 29 2025 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.01~beta-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_42_Mass_Rebuild

* Fri Aug 02 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.01~beta-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_41_Mass_Rebuild

* Sun Feb 04 2024 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.01~beta-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_40_Mass_Rebuild

* Fri Aug 11 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 5.01~beta-4
- fix check for libgs.so to avoid spurious output

* Fri Aug 11 2023 Andrew Bauer <zonexpertconsulting@outlook.com> - 5.01~beta-4
- Fix check for libgs.so to allow for two digit rev
- use autosetup macro

* Thu Aug 03 2023 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.01~beta-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_39_Mass_Rebuild

* Mon Aug 08 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 5.01~beta-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_37_Mass_Rebuild and ffmpeg
  5.1

* Wed May 25 2022 Sérgio Basto <sergio@serjux.com> - 5.01~beta-1
- 5.01beta  (what a waste of time) doesn't work

* Thu Feb 10 2022 RPM Fusion Release Engineering <sergiomb@rpmfusion.org> - 4.9-18
- Rebuilt for https://fedoraproject.org/wiki/Fedora_36_Mass_Rebuild

* Wed Aug 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-17
- Rebuilt for https://fedoraproject.org/wiki/Fedora_35_Mass_Rebuild

* Thu Feb 04 2021 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_34_Mass_Rebuild

* Wed Aug 19 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_33_Mass_Rebuild

* Wed Feb 05 2020 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-14
- Rebuilt for https://fedoraproject.org/wiki/Fedora_32_Mass_Rebuild

* Sat Aug 10 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Tue Mar 05 2019 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-12
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Aug 19 2018 RPM Fusion Release Engineering <leigh123linux@gmail.com> - 4.9-11
- Rebuilt for Fedora 29 Mass Rebuild binutils issue

* Fri Jul 27 2018 RPM Fusion Release Engineering <sergio@serjux.com> - 4.9-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Mar 12 2018 Leigh Scott <leigh123linux@googlemail.com> - 4.9-9
- Clean and fix

* Fri Mar 02 2018 RPM Fusion Release Engineering <leigh123linux@googlemail.com> - 4.9-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Aug 31 2017 RPM Fusion Release Engineering <kwizart@rpmfusion.org> - 4.9-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sun Aug 31 2014 Sérgio Basto <sergio@serjux.com> - 4.9-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Tue Mar 12 2013 Nicolas Chauvet <kwizart@gmail.com> - 4.9-5
- https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Thu Feb 09 2012 Nicolas Chauvet <kwizart@gmail.com> - 4.9-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed May 04 2011 Rex Dieter <rdieter@fedoraproject.org> 4.9-3
- Recompile gsview against newer ghostscript (#1737)

* Wed Nov 11 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4.9-2
- rebuild after movement to RPM Fusion nonfree

* Thu Oct 22 2009 Rex Dieter <rdieter@fedoraproject.org> 4.9-1
- gsview-4.9
- optimize scriptlets
- use xdg-open (instead of htmlview)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 4.8-5
- rebuild for new F11 features

* Mon Sep 15 2008 Rex Dieter <rdieter@fedoraproject.org> 4.8-4
- cleanup .desktop file bits

* Sun Aug 03 2008 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info - 4.8-3
- rebuild

* Tue Oct 10 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.8-2
- respin

* Sun May 07 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.8-1
- 4.8

* Mon Apr 17 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-7
- rework for Livna

* Wed Mar 1 2006 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-6
- %%(rpm -q --qf '%%{VERSION}' ghostscript) -> %%(gs --version)
- follow fdo icon spec
- restore epstool bits

* Fri Feb 10 2006 Rex Dieter <rexdieter[AT]users.sf.net>
- fc5: gcc/glibc respin

* Fri Oct 21 2005 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-5
- %%post/%%postun: update-desktop-database 

* Fri Aug  5 2005 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-4
- ExcludeArch: ppc (sed busted?)

* Thu Jul 28 2005 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-3
- add file:// to help URL.

* Thu Jun 23 2005 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-2
- fixes for ghostscript-8.15 (#159912)
- Change paper default A4->Letter

* Wed Apr 20 2005 Rex Dieter <rexdieter[AT]users.sf.net> 4.7-1
- 4.7

* Fri Apr  7 2005 Michael Schwendt <mschwendt[AT]users.sf.net>
- rebuilt

* Wed Jan 26 2005 Rex Dieter <rexdieter[AT]users.sf.net> 0:4.6-9
- back to Req: ghostscript >= 7.07-15.3 for x86_64 (#146223)

* Fri Aug 06 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.8
- Patch to load libgs.so.7 by default (instead of libgs.so)
- Req: libgs.so.7, dropping Req: ghostscript, allowing for users
  with older/custom ghostscript builds (will have to rework when/if
  ghostscript >= 8.0 comes)
- .desktop: GenericName: PS/PDF Viewer

* Thu Aug 05 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.7
- remove Req: libgs.so
- Req: ghostscript >= 7.07-15.3
  (http://www.redhat.com/archives/fedora-devel-list/2004-August/msg00068.html)

* Tue Aug 03 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.6
- Requires: ghostscript >= 7.07-18

* Thu Apr 29 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.5
- Group: Applications/Publishing
- remove Vendor tag

* Sat Apr 24 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.4
- gsview.desktop: StartupWMClass=gsview

* Sat Apr 24 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.3
- don't include old epstool (to be packaged separately)
- gsview.desktop: 
  MimeType=image/x-eps;application/postscript;application/pdf; 
  Categories=Application;GTK;Graphics;Viewer;Publishing;

* Thu Apr 01 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.2
- desktop-file default
- patch default .desktop file for Categories

* Tue Jan 20 2004 Rex Dieter <rexdieter at sf.net> 0:4.6-0.fdr.1
- 4.6
- desktop_file'ize

* Fri Oct 31 2003 Rex Dieter <rexdieter at sf.net> 0:4.5-0.fdr.1
- 4.5
- Fedora Core support

* Thu Jul 03 2003 Rex Dieter <rexdieter at sf.net> 0:4.4-0.fdr.0
- fedora'ize
- htmlview patch
