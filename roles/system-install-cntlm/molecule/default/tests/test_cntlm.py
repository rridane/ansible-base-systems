def test_cntlm_binary_exists(host):
    cntlm_bin = host.file("/usr/local/sbin/cntlm")

    vars = host.ansible.get_variables()
    state = vars.get("cntlm_state", []) or []

    if state == 'absent':
        assert not cntlm_bin.exists

        return

    assert cntlm_bin.exists
    assert cntlm_bin.is_file
    assert cntlm_bin.mode == 0o755

def test_cntlm_config_file(host):
    config = host.file("/etc/cntlm.conf")

    vars = host.ansible.get_variables()
    state = vars.get("cntlm_state", []) or []

    if state == 'absent':
        assert not config.exists

        return

    assert config.exists
    assert config.is_file
    assert config.mode == 0o644
    assert config.user == "root"
    assert config.group == "root"

def test_cntlm_config_content(host):
    config = host.file("/etc/cntlm.conf")

    vars = host.ansible.get_variables()
    state = vars.get("cntlm_state", []) or []

    if state == 'absent':
        assert not config.exists

        return

    assert config.contains("Username    svc-proxy")
    assert config.contains("PassNTLMv2  AABBCCDDEEFF00112233445566778899")
    assert config.contains("Listen      3128")
    assert config.contains("Proxy       proxy.acme.corp:8080")
    assert config.contains("NoProxy     localhost, 127.0.0.1, .svc, .cluster.local")
    assert config.contains("Auth NTLMv2")
    assert config.contains("Allow 10.*")

# def test_cntlm_service(host):
#     service = host.service("cntlm")
#     assert service.is_running
#     assert service.is_enabled
#
# def test_cntlm_socket(host):
#     socket = host.socket("tcp://0.0.0.0:3128")
#     assert socket.is_listening
