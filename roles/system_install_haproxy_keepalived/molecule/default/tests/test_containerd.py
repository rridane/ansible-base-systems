# tests/test_haproxy.py
import re
import pytest

def _vars(host):
    return host.ansible.get_variables()

# -----------------------------
# HAProxy
# -----------------------------
def test_haproxy_service_running_enabled(host):
    svc = host.service("haproxy")
    assert svc.is_enabled
    assert svc.is_running

def test_haproxy_config_exists_and_validates(host):
    cfg = host.file("/etc/haproxy/haproxy.cfg")
    assert cfg.exists
    assert cfg.is_file

    # sanity: quelques directives clés attendues
    assert cfg.contains(r"^global")
    assert cfg.contains(r"^defaults")
    assert cfg.contains(r"^frontend stats")
    assert cfg.contains(r"http-request use-service prometheus-exporter")

    # validation de la conf (comme ton handler)
    res = host.run("haproxy -c -f /etc/haproxy/haproxy.cfg")
    assert res.rc == 0, f"haproxy -c failed: {res.stdout}\n{res.stderr}"

def test_haproxy_admin_socket_present(host):
    sock = host.file("/run/haproxy/admin.sock")
    # Le socket n'existe qu'une fois le service démarré
    assert sock.exists
    assert sock.is_socket

def test_haproxy_stats_frontend_listening(host):
    v = _vars(host)
    port = str(v.get("haproxy_frontend_stats_port", "")).strip()
    if not port:
        pytest.skip("haproxy_frontend_stats_port non défini")
    # écoute en 0.0.0.0:* (container systemd geerlingguy expose en local)
    s = host.socket(f"tcp://0.0.0.0:{port}")
    assert s.is_listening

def test_haproxy_cfg_renders_users_and_mode(host):
    import re
    v = host.ansible.get_variables()
    username = v.get("haproxy_username", "haproxy")
    groupname = v.get("haproxy_groupname", "haproxy")
    default_mode = v.get("haproxy_default_mode", "tcp")

    cfg = host.file("/etc/haproxy/haproxy.cfg")
    text = cfg.content_string

    assert re.search(rf"\buser\s+{re.escape(str(username))}\b", text)
    assert re.search(rf"\bgroup\s+{re.escape(str(groupname))}\b", text)

    # accept mode in defaults or any frontend
    mode_pat = rf"\bmode\s+{re.escape(str(default_mode))}\b"
    has_defaults_mode = re.search(rf"(?ms)^\s*defaults\b.*?^\s*{mode_pat}", text) is not None
    has_frontend_mode = re.search(rf"(?ms)^\s*frontend\b.*?{mode_pat}", text) is not None
    assert has_defaults_mode or has_frontend_mode, f"Couldn't find '{default_mode}' mode:\n{text}"

def test_haproxy_backends_rendered(host):
    import re
    v = host.ansible.get_variables()
    cfg = host.file("/etc/haproxy/haproxy.cfg")
    text = cfg.content_string

    # masters pour api-server-backend
    for m in v.get("masters", []) or []:
        hostname, ip, port = m.get("hostname"), m.get("ip"), m.get("port")
        if not all([hostname, ip, port]):
            continue
        # ^\s*server <host> <ip>:<port> ... check ...
        pattern = rf"(?m)^\s*server\s+{re.escape(hostname)}\s+{re.escape(ip)}:{port}\b.*\bcheck\b"
        assert re.search(pattern, text), f"Missing server line for master: {hostname}\n{text}"

    # nodes pour traefik-backend
    for n in v.get("nodes", []) or []:
        hostname, ip, port = n.get("hostname"), n.get("ip"), n.get("port")
        if not all([hostname, ip, port]):
            continue
        pattern = rf"(?m)^\s*server\s+{re.escape(hostname)}\s+{re.escape(ip)}:{port}\b.*\bcheck\b"
        assert re.search(pattern, text), f"Missing server line for node: {hostname}\n{text}"


def test_haproxy_frontends_listening(host):
    v = _vars(host)

    api_port = v.get("api_server_frontend_port")
    if api_port:
        s = host.socket(f"tcp://0.0.0.0:{api_port}")
        assert s.is_listening

    traefik_port = v.get("traefik_frontend_port")
    if traefik_port:
        s = host.socket(f"tcp://0.0.0.0:{traefik_port}")
        assert s.is_listening

# # -----------------------------
# # Keepalived
# # -----------------------------
def test_keepalived_service_running_enabled(host):
    svc = host.service("keepalived")
    assert svc.is_enabled
    assert svc.is_running

def test_keepalived_config_exists_and_validates(host):
    import re
    v = host.ansible.get_variables()
    cfg = host.file("/etc/keepalived/keepalived.conf")
    assert cfg.exists
    assert cfg.is_file

    text = cfg.content_string

    # vrrp_instance VI_1 présent
    assert re.search(r"\bvrrp_instance\s+VI_1\b", text), text

    # interface (si var fournie)
    if v.get("keepalived_interface"):
        iface = str(v["keepalived_interface"])
        assert re.search(rf"\binterface\s+{re.escape(iface)}\b", text), text

    # VIP (si var fournie)
    if v.get("ha_vip"):
        vip = str(v["ha_vip"])
        assert vip in text, text

    # (optionnel) rôle si tu le passes en host_vars (MASTER/BACKUP)
    role = v.get("keepalived_role")
    if role:
        assert re.search(rf"\bstate\s+{re.escape(str(role))}\b", text), text

    # validation de la conf (comme ton handler)
    res = host.run("keepalived -t -f /etc/keepalived/keepalived.conf")
    assert res.rc == 0, f"keepalived -t failed: {res.stdout}\n{res.stderr}\n{text}"