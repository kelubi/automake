RPMBUILD_PAT=/root/lnmpp/rpmbuild
echo "%_topdir   $RPMBUILD_PAT" > ~/.rpmmacros
mkdir -p $RPMBUILD_PAT/{BUILD,RPMS,SOURCES,SPECS,SRPMS}
mkdir -p $RPMBUILD_PAT/RPMS/{noarch,i386,i686,x86_64}
find $RPMBUILD_PAT