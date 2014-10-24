#!/usr/bin/env python

import argparse
import em
import errno
import os
import re
import shutil
import subprocess
import tempfile


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_dsc_file(dirpath):
    dlist = os.listdir(dirpath)

    fname = None
    for f in dlist:
        if f.endswith('.dsc'):
            fname = f

    if not fname:
        raise Exception("no dsc file found in %s" % dlist)
    return os.path.join(dirpath, fname)


def get_build_depends(dsc_file):
    with open(dsc_file, 'r') as fh:
        dsc_lines = fh.readlines()

    build_depends_string = [d.strip() for d in dsc_lines
                            if d.startswith('Build-Depends')]

    if len(build_depends_string) not in [1, 2]:
        raise Exception("Failed to find one or two Build-Depends in %s. " % (dsc_lines))

    deps = [e.split(': ')[1] for e in build_depends_string]
    ind = [e.split(', ') for e in deps]

    alldeps = set()
    for l in ind:
        alldeps |= set(l)
    alldeps = [re.sub('[() ]', '', e) for e in alldeps]
    return alldeps

parser = argparse.ArgumentParser(description="Build a debian package")
parser.add_argument('package', nargs='+')
parser.add_argument('--config-file', '-c', dest='config', default=None)
parser.add_argument('--os', dest='os', default='ubuntu')
parser.add_argument('--codename', dest='codename', default='trusty')

args = parser.parse_args()

print("args", args)


for package in args.package:
    image_name = 'dbuilder-%s-%s' % (args.codename, package)

    # todo use real temp file
    tempdir = 'foo-%s' % package

    sourcedir = os.path.join(tempdir, 'src')
    mkdir_p(sourcedir)
    src_cmd = ['apt-get', 'source', package]
    subprocess.check_call(src_cmd, cwd=sourcedir)
    dsc_file = get_dsc_file(sourcedir)
    print(dsc_file, " dsc file")
    build_deps = get_build_depends(dsc_file)
    print("BUild DEPENDS", build_deps)

    dockerfile = os.path.join(tempdir, 'Dockerfile')

    with open(dockerfile, 'w') as df:
        t = open('Dockerfile.em', 'r').read()
        d = {
            'codename': args.codename,
            'os': args.os,
            'build_depends': sorted(build_deps),
        }
        df.write(em.expand(t, d))
    shutil.copy2('dbuilder.sh', os.path.join(tempdir, 'dbuilder.sh'))

    build_cmd = ['docker', 'build', '-t', image_name, '.']
    subprocess.check_call(build_cmd, cwd=tempdir)



    run_cmd = ['docker', 'run', '-ti', '-v', '/tmp/output:/output', image_name, package]
    print(run_cmd)
    subprocess.check_call(run_cmd, cwd=tempdir)
