#!/usr/bin/env python

import argparse
import em
import os
import shutil
import subprocess
# import tempfile

parser = argparse.ArgumentParser(description="Build a debian package")
parser.add_argument('package', nargs='+')
parser.add_argument('--config-file', '-c', dest='config', default=None)
parser.add_argument('--os', dest='os', default='ubuntu')
parser.add_argument('--codename', dest='codename', default='trusty')

args = parser.parse_args()

print("args", args)

image_name = 'dbuilder-%s' % args.codename

# todo use real temp file
tempdir = 'foo'

dockerfile = os.path.join(tempdir, 'Dockerfile')

with open(dockerfile, 'w') as df:
    t = open('Dockerfile.em', 'r').read()
    d = {
        'codename': args.codename,
        'os': args.os
    }
    df.write(em.expand(t, d))
shutil.copy2('dbuilder.sh', 'foo/dbuilder.sh')

build_cmd = ['docker', 'build', '-t', image_name, '.']
subprocess.check_call(build_cmd, cwd=tempdir)


for package in args.package:
    run_cmd = ['docker', 'run', '-ti', '-v', '/tmp/output:/output', image_name, package]
    print(run_cmd)
    subprocess.check_call(run_cmd, cwd=tempdir)
