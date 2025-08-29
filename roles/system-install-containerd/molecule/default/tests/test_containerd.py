def test_containerd_service(host):
    svc = host.service('containerd')
    assert svc.is_running
    assert svc.is_enabled


def test_containerd_config(host):
    config = host.file('/etc/containerd/config.toml')
    assert config.exists
    assert config.contains('root = "/mnt/data/containerd"')
    assert config.contains('systemd_cgroup = true')


def test_registry_configs(host):
    registry1 = host.file('/etc/containerd/certs.d/10.212.22.8:5600/hosts.toml')
    assert registry1.exists
    assert registry1.contains('server = "http://10.212.22.8:5600"')
    assert registry1.contains('skip_verify = true')

    registry2 = host.file('/etc/containerd/certs.d/10.212.22.8:5500/hosts.toml')
    assert registry2.exists
    assert registry2.contains('server = "http://10.212.22.8:5500"')

def test_containerd_version(host):
    vars = host.ansible.get_variables()
    inventory_hostname = vars.get("inventory_hostname", "")

    cmd = host.run("containerd --version")

    if inventory_hostname == "ubuntu-22-version-32":
        pinned = vars.get("containerd_version", "")

        if pinned:
            upstream = pinned.split("-", 1)[0]  # drop debian revision
            assert upstream in cmd.stdout
    else:
        assert cmd.succeeded