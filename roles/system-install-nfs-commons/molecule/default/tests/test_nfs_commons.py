import pytest

def test_nfs_package_installed(host):
    """
    Vérifie que le paquet NFS client est installé.
    """
    distro = host.system_info.distribution.lower()
    if "debian" in distro or "ubuntu" in distro:
        pkg = host.package("nfs-common")
    else:
        # Pour EL / Rocky / CentOS
        pkg = host.package("nfs-utils")

    assert pkg.is_installed, f"NFS package not installed on {distro}"


@pytest.mark.parametrize("bin_path", [
    "/usr/sbin/mount.nfs",
    "/usr/sbin/showmount",
])
def test_nfs_binaries_exist_and_executable(host, bin_path):
    """
    Vérifie que les binaires NFS existent et sont exécutables.
    """
    f = host.file(bin_path)
    assert f.exists, f"{bin_path} should exist"
    assert f.is_file, f"{bin_path} should be a file"
    assert f.mode & 0o111, f"{bin_path} should be executable"
