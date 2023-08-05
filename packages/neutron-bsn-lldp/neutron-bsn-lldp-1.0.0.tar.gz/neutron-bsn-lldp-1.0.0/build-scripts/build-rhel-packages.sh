#!/bin/bash
# Copyright 2018 Big Switch Networks, Inc.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.
set -eux

DOCKER_IMAGE=$DOCKER_REGISTRY'/horizon-bsn-builder:latest'
BUILD_OS=centos7-x86_64
CURR_VERSION=$(awk '/^version/{print $3}' setup.cfg)

docker pull $DOCKER_IMAGE

BUILDDIR=$(mktemp -d)
mkdir -p $BUILDDIR/{BUILD,BUILDROOT,RPMS,SOURCES,SPECS,SRPMS}

cp dist/* $BUILDDIR/SOURCES/
cp rhel/*.service $BUILDDIR/SOURCES/
cp rhel/*.spec $BUILDDIR/SPECS/
cp build-scripts/build-rhel-packages-inner.sh $BUILDDIR/build-rhel-packages-inner.sh

docker run -v $BUILDDIR:/rpmbuild $DOCKER_IMAGE /rpmbuild/build-rhel-packages-inner.sh

# Copy built RPMs to pkg/
OUTDIR=$(readlink -m "pkg/$BUILD_OS/$GIT_BRANCH/$CURR_VERSION")
rm -rf "$OUTDIR" && mkdir -p "$OUTDIR"
mv $BUILDDIR/SRPMS/*.rpm "$OUTDIR"
mv $BUILDDIR/RPMS/noarch/*.rpm "$OUTDIR"
cp dist/*.tar.gz "$OUTDIR"
git log > "$OUTDIR/gitlog.txt"
touch "$OUTDIR/build-$CURR_VERSION"
ln -snf $(basename $OUTDIR) $OUTDIR/../latest

rm -rf "$BUILDDIR"
