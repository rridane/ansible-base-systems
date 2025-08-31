import os
import pytest

CNI_DIR = "/etc/cni/net.d"
CALICO_CONF_FILES = (
    "/etc/cni/net.d/10-calico.conflist",
    "/etc/cni/net.d/calico.conflist",
    "/etc/cni/net.d/calico-kubeconfig",
)
CALICO_BINS = (
    "/opt/cni/bin/calico",
    "/opt/cni/bin/calico-ipam",
)
CALICO_STATE_DIRS = (
    "/var/lib/cni/networks",
    "/var/lib/calico",
)
CNI_IFACES = ("cni0", "flannel.1", "tunl0", "vxlan.calico")
KUBE_PKGS = ("kubeadm", "kubelet", "kubectl")


def _vars(host):
    """Récupère les variables Ansible avec des défauts cohérents."""
    v = host.ansible.get_variables()
    return {
        "kube_cleanup_enabled": bool(v.get("kube_cleanup_enabled", True)),
        "kube_cleanup_packages": bool(v.get("kube_cleanup_packages", True)),
        "kube_cleanup_cni": bool(v.get("kube_cleanup_cni", True)),
        "kube_cleanup_calico": bool(v.get("kube_cleanup_calico", True)),
    }


def _is_debian_like(host):
    return host.system_info.distribution.lower() in ("debian", "ubuntu")


# ----------------------------- PACKAGES ------------------------------------- #

def test_kube_packages_absent_when_enabled(host):
    """Si kube_cleanup_packages=true, les paquets kube doivent être absents."""
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_packages"]:
        pytest.skip("Cleanup packages désactivé.")

    if not _is_debian_like(host):
        pytest.skip("Test packages conçu pour Debian/Ubuntu (APT).")

    for name in KUBE_PKGS:
        pkg = host.package(name)
        assert not pkg.is_installed, f"Le paquet {name} devrait être absent."


# ----------------------------- CNI ------------------------------------------ #

def test_cni_config_dir_absent_when_enabled(host):
    """Le répertoire /etc/cni/net.d doit être supprimé si kube_cleanup_cni=true."""
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_cni"]:
        pytest.skip("Cleanup CNI désactivé.")

    cni = host.file(CNI_DIR)
    assert not cni.exists, f"{CNI_DIR} devrait être absent."


def test_cni_interfaces_absent_when_enabled(host):
    """Les interfaces CNI connues ne doivent pas exister (best effort)."""
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_cni"]:
        pytest.skip("Cleanup CNI désactivé.")

    for iface in CNI_IFACES:
        cmd = host.run(f"ip link show {iface}")
        assert cmd.rc != 0, f"L'interface {iface} ne devrait pas exister (rc={cmd.rc})."


# ----------------------------- CALICO --------------------------------------- #

def test_calico_conf_bins_state_absent_when_enabled(host):
    """Fichiers de conf, binaires et répertoires d'état Calico doivent être absents."""
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_calico"]:
        pytest.skip("Cleanup Calico désactivé.")

    for p in CALICO_CONF_FILES:
        assert not host.file(p).exists, f"{p} devrait être absent"

    for p in CALICO_BINS:
        assert not host.file(p).exists, f"{p} devrait être absent"

    for d in CALICO_STATE_DIRS:
        assert not host.file(d).exists, f"{d} devrait être absent"


def test_no_cali_veth_leftovers(host):
    """Aucune interface veth commençant par 'cali' ne doit rester."""
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_calico"]:
        pytest.skip("Cleanup Calico désactivé.")

    cmd = host.run("bash -lc \"ip -o link show | awk -F': ' '/^[0-9]+: cali/{print $2}'\"")
    assert cmd.rc == 0, f"Commande ip link show a échoué: {cmd.stderr}"
    assert cmd.stdout.strip() == "", f"Interfaces cali* restantes: {cmd.stdout}"


def test_no_cali_iptables_chains(host):
    """
    Aucune chaîne iptables 'cali-*' ne doit rester (filter/nat/mangle).
    Skip si iptables n'est pas présent (ex: images minimales).
    """
    v = _vars(host)
    if not v["kube_cleanup_enabled"] or not v["kube_cleanup_calico"]:
        pytest.skip("Cleanup Calico désactivé.")

    # Vérifie la présence d'iptables
    have_iptables = host.run("bash -lc 'command -v iptables'").rc == 0
    if not have_iptables:
        pytest.skip("iptables non disponible dans l'image de test.")

    for table in ("filter", "nat", "mangle"):
        cmd = host.run(f"bash -lc \"iptables -t {table} -S | awk '/-N cali-/'\"")
        assert cmd.rc in (0, 1), f"iptables -S rc={cmd.rc} err={cmd.stderr}"
        # Pas de lignes ' -N cali-...'
        assert cmd.stdout.strip() == "", f"Chaînes 'cali-*' restantes dans la table {table} : {cmd.stdout}"
