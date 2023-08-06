# Copyright (c) Microsoft Corporation. All rights reserved.
import copy
import distro
import glob
import os
import re
import shutil
import subprocess
import sys
from typing import List, Optional


__version__ = '2.1.2'   # {major dotnet version}.{minor dotnet version}.{revision}
# We can rev the revision due to patch-level change in .net or changes in dependencies
missing_dep_re = re.compile(r'^(.+)\s*=>\s*not found\s*$', re.MULTILINE)


# https://github.com/dotnet/core/blob/master/Documentation/self-contained-linux-apps.md
# to evalute mappings candidates, run this cmd over the expanded dotnetcore runtime zip:
#   find . -name '*.so' | xargs ldd | less
# search for 'not found'.
ubuntu_mappings = {
    'libunwind-x86_64.so.8': 'libunwind8=1.1-4.1',
    'libunwind.so.8': 'libunwind8=1.1-4.1',
    'liblttng-ust.so.0': 'liblttng-ust0=2.7.1-1',
    'libcurl.so.4': 'libcurl3=7.47.0-1ubuntu2',
    'liburcu-bp.so.4': 'liburcu4=0.9.1-3',
    'liburcu-cds.so.4': 'liburcu4=0.9.1-3'
}

rhel_mappings = {
    'liblttng-ust.so.0': 'rh-dotnet21-lttng-ust.x86_64',
    'liburcu-bp.so.4': 'rh-dotnet21-userspace-rcu.x86_64',
    'liburcu-cds.so.4': 'rh-dotnet21-userspace-rcu.x86_64',
    'libcurl.so.4': 'rh-dotnet21-curl.x86_64'
}

distro = distro.linux_distribution(full_distribution_name=False)[0] if sys.platform == 'linux' else None


def _get_mappings():
    if distro == 'ubuntu':
        return ubuntu_mappings
    if distro == 'rhel':
        return rhel_mappings
    else:
        raise ValueError('Unsupported Linux distribution {0}'.format(distro))

def _get_dependency_pkg_name(dependency: str) -> str:
    dep_mappings = _get_mappings()
    if dependency not in dep_mappings:
        raise ValueError('Required dependency missing: ' + dependency)

    return dep_mappings[dependency]


def _gather_dependencies(path: str, search_path: str=None) -> List[str]:
    libraries = glob.glob(os.path.realpath(os.path.join(path, '**', '*.so')), recursive=True)
    missing_deps = set()
    env = copy.copy(os.environ)
    if search_path is not None:
        env['LD_LIBRARY_PATH'] = search_path
    for library in libraries:
        ldd_output = subprocess.run(['ldd', library], cwd=path, stdout=subprocess.PIPE, env=env).stdout.decode('utf-8')
        matches = missing_dep_re.findall(ldd_output)
        missing_deps |= set(dep.strip() for dep in matches)

    missing_dep_pkgs = set(_get_dependency_pkg_name(dep) for dep in missing_deps)

    return [d for d in missing_dep_pkgs]


def _install_dependency(pkg_name: str, target_path: str):
    download_folder = os.path.join(_get_pkg_download_folder(), pkg_name)
    os.makedirs(download_folder, exist_ok=True)
    downloader = _get_pkg_fetcher()
    downloader(pkg_name, download_folder)
    lib_files = glob.glob(os.path.join(download_folder, '**', '*.so*'), recursive=True)
    for file in lib_files:
        shutil.copy(file, target_path)

def _get_pkg_download_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin', 'tmp')


def _get_bin_folder() -> str:
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin')


def ensure_dependencies() -> Optional[str]:
    if distro is None:
        return None

    bin_folder = _get_bin_folder()
    deps_path = os.path.join(bin_folder, 'deps')
    success_file = os.path.join(deps_path, 'SUCCESS-' + __version__)
    if os.path.exists(success_file):
        return deps_path

    os.makedirs(deps_path, exist_ok=True)
    while True:
        missing_pkgs = _gather_dependencies(bin_folder, search_path=deps_path)
        if not missing_pkgs:
            break

        for pkg in missing_pkgs:
            _install_dependency(pkg, deps_path)

    shutil.rmtree(_get_pkg_download_folder(), ignore_errors=True)
    with open(success_file, 'a'):
        os.utime(success_file, None)
    return deps_path


def get_runtime_path():
    search_string = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'bin', 'dotnet*')
    matches = [f for f in glob.glob(search_string, recursive=True)]
    return matches[0]


def _get_pkg_fetcher():
    if distro == 'ubuntu':
        return _fetch_deb_package
    if distro == 'rhel':
        return _fetch_yum_package
    else:
        return None

def _fetch_deb_package(pkg_name: str, download_folder: str):
    subprocess.run(['apt-get', 'download', pkg_name], cwd=download_folder)
    subprocess.run(['ar', 'x', glob.glob(os.path.join(download_folder, '*.deb'))[0]], cwd=download_folder)
    subprocess.run(['tar', 'xf', 'data.tar.xz'], cwd=download_folder)

def _fetch_yum_package(pkg_name: str, download_folder: str):
    # gather package info needed for download from repo:
    pkg_info = subprocess.run(['yum', 'info', pkg_name], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, check=True).stdout.decode('utf-8')
    repo_name_re = re.compile(r'^Repo\s*:\s*([a-zA-Z0-9_-]+)', re.MULTILINE)
    repo_name = repo_name_re.search(pkg_info)[1]
    if not repo_name:
        raise ValueError('Cannot find yum repo info for {0}'.format(pkg_name))

    repo_config_file = subprocess.run(['grep', '-F', '--color=never', '-l', '-r', repo_name, '/etc/yum.repos.d/'], stdout=subprocess.PIPE, check=True) \
        .stdout.decode('utf-8')
    if not repo_config_file:
        raise ValueError('Cannot find repo {0} in repo config files.'.format(repo_name))

    # parse out repo authN certificates from config:
    cert_file = ''
    key_file = ''
    with open(repo_config_file.strip(), 'r') as config:
        found_block = False
        for line in config:
            if found_block:
                if line.isspace():
                    break
                else:
                    line = line.strip()
                    if line.startswith('sslclientcert'):
                        cert_file = line.split('=')[1]
                    if line.startswith('sslclientkey'):
                        key_file = line.split('=')[1]
            else:
                if line.find(repo_name) >= 0:
                    found_block = True

    pkgUrl = subprocess.run(['repoquery', '--location', pkg_name], stdout=subprocess.PIPE, check=True).stdout.decode('utf-8').strip()

    if not _wget(pkgUrl, cert_file, key_file, download_folder):
        if not _wget(pkgUrl, cert_file, key_file, download_folder, use_sudo=True):
            raise ValueError('Cannot download yum package {0}'.format(pkgUrl))

    # extract files:
    rpmProc = subprocess.Popen(['rpm2cpio', os.path.basename(pkgUrl)], stdout=subprocess.PIPE, cwd=download_folder)
    cpioProc = subprocess.Popen(['cpio', '-idmv'], stdin=rpmProc.stdout, stdout=subprocess.PIPE, cwd=download_folder)
    rpmProc.stdout.close()
    cpioProc.communicate()

def _wget(url: str, cert: str, key: str, cwd: str, use_sudo: bool=False) -> bool:
    wget_cmd = [ 'wget' ]
    if use_sudo:
        wget_cmd.insert(0, 'sudo')
    if cert and key:
        wget_cmd.extend([ '--no-check-certificate', '--certificate={}'.format(cert), '--private-key={}'.format(key)])
    wget_cmd.append(url)
    out = subprocess.run(wget_cmd, stderr=subprocess.PIPE, cwd=cwd, check=False).stderr.decode('utf-8')
    return out.find('200 OK') >= 0
