def test_conf_files_are_present(host):

    apt_proxy_file = host.file("/etc/apt/apt.conf.d/99-proxy.conf")
    systemd_dropin_file = host.file("/etc/systemd/system.conf.d/10-proxy.conf")

    assert apt_proxy_file.exists
    assert apt_proxy_file.is_file

    assert systemd_dropin_file.exists
    assert systemd_dropin_file.is_file


def test_conf_file_content(host):

    apt_proxy_file = host.file("/etc/apt/apt.conf.d/99-proxy.conf")
    systemd_dropin_file = host.file("/etc/systemd/system.conf.d/10-proxy.conf")
    etc_environment_file = host.file("/etc/environment")

    apt_proxy_file_content = apt_proxy_file.content_string
    systemd_dropin_file_content = systemd_dropin_file.content_string
    etc_environment_file_content = etc_environment_file.content_string

    assert "DefaultEnvironment=\"HTTP_PROXY=monproxy.monproxy.org\" \"HTTPS_PROXY=monproxy.monproxy.org\" \"NO_PROXY=127.0.0.1,localhost,.svc,.cluster.local" in systemd_dropin_file_content
    assert "Acquire::https::Proxy \"monproxy.monproxy.org\"" in apt_proxy_file_content;

    assert "HTTP_PROXY=\"monproxy.monproxy.org\"" in etc_environment_file_content
    assert "http_proxy=\"monproxy.monproxy.org\"" in etc_environment_file_content
    assert "HTTPS_PROXY=\"monproxy.monproxy.org\"" in etc_environment_file_content
    assert "https_proxy=\"monproxy.monproxy.org\"" in etc_environment_file_content
    assert "NO_PROXY=\"127.0.0.1,localhost,.svc,.cluster.local\"" in etc_environment_file_content
    assert "no_proxy=\"127.0.0.1,localhost,.svc,.cluster.local\"" in etc_environment_file_content