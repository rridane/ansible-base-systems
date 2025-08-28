import os
import re
import pytest


KUBE_APT_LIST = "/etc/apt/sources.list.d/kubernetes.list"
KUBE_KEYRING_DIR = "/etc/apt/keyrings"
KUBE_KEYRING = "/etc/apt/keyrings/kubernetes-archive-keyring.gpg"
CNI_DIR = "/etc/cni/net.d"
PKGS = ("kubeadm", "kubelet", "kubectl")


def _vars(host):
    """Raccourci : variables Ansible visibles par Testinfra."""
    v = host.ansible.get_variables()
    # Valeurs par défaut alignées avec le rôle
    return {
        "kube_state": (v.get("kube_state") or "present").strip(),
        "kube_version": v.get("kube_version") or "",
        "kube_cri_socket": v.get("kube_cri_socket") or "/var/run/containerd/containerd.sock",
    }


def _is_debian_like(host):
    return host.system_info.distribution.lower() in ("debian", "ubuntu")


@pytest.mark.skipif(True, reason="Ces tests sont conçus pour Debian/Ubuntu (APT).")
def test_guard_never_runs():
    """Garde technique: ce test est skippé par défaut pour éviter des faux positifs si déplacé."""
    pass


def test_packages_state(host):
    """
    present  -> kubeadm/kubelet/kubectl installés (avec version si pinning demandé).
    absent   -> paquets non installés.
    """
    if not _is_debian_like(host):
        pytest.skip("Tests APT seulement (Debian/Ubuntu).")

    v = _vars(host)
    for name in PKGS:
        pkg = host.package(name)
        if v["kube_state"] == "present":
            assert pkg.is_installed, f"{name} devrait être installé quand kube_state=present"

            # Si kube_version est spécifiée, vérifie la version exacte (préfixe OK : '1.29.4-00'…)
            if v["kube_version"]:
                # Sur Debian/Ubuntu, testinfra renvoie 'version' (ex: '1.29.4-00')
                assert pkg.version.startswith(v["kube_version"]), (
                    f"{name} version '{pkg.version}' ne correspond pas à '{v['kube_version']}'"
                )
        else:
            assert not pkg.is_installed, f"{name} ne devrait PAS être installé quand kube_state=absent"


def test_repo_and_key_when_present(host):
    """
    present -> fichier de repo + keyring existent et contiennent la bonne ligne.
    absent  -> on NE FAIT PAS d'assertion (le rôle ne supprime pas le repo).
    """
    if not _is_debian_like(host):
        pytest.skip("Tests APT seulement (Debian/Ubuntu).")

    v = _vars(host)
    if v["kube_state"] != "present":
        pytest.skip("Repo et key non requis quand kube_state=absent.")

    # Keyring dir + keyring
    d = host.file(KUBE_KEYRING_DIR)
    assert d.exists and d.is_directory, f"{KUBE_KEYRING_DIR} devrait exister"

    k = host.file(KUBE_KEYRING)
    assert k.exists and k.is_file, f"{KUBE_KEYRING} devrait exister"

    # Repo list file
    lst = host.file(KUBE_APT_LIST)
    assert lst.exists and lst.is_file, f"{KUBE_APT_LIST} devrait exister"

    content = lst.content_string.strip()
    # Ligne attendue (tolère espaces multiples)
    expected = (
        r"^deb\s+\[signed-by=/etc/apt/keyrings/kubernetes-archive-keyring\.gpg\]\s+"
        r"https?://apt\.kubernetes\.io/\s+kubernetes-xenial\s+main\s*$"
    )
    assert re.search(expected, content, re.MULTILINE), (
        f"Contenu de {KUBE_APT_LIST} inattendu.\nTrouvé:\n{content}"
    )


def test_cni_state_when_absent(host):
    """
    absent -> /etc/cni/net.d supprimé, interfaces CNI inexistantes (cni0, flannel.1).
    present -> pas d'exigence (le rôle n'installe pas de CNI).
    """
    v = _vars(host)
    if v["kube_state"] != "absent":
        pytest.skip("Vérif CNI seulement quand kube_state=absent.")

    # Répertoire de config CNI supprimé
    cni = host.file(CNI_DIR)
    assert not cni.exists, f"{CNI_DIR} devrait être absent quand kube_state=absent"

    # Interfaces réseau CNI absentes (ou commande renvoie rc != 0)
    for iface in ("cni0", "flannel.1"):
        cmd = host.run(f"ip link show {iface}")
        assert cmd.rc != 0, f"L'interface {iface} ne devrait pas exister (rc={cmd.rc})"


def test_kubeadm_binary_presence(host):
    """
    present -> kubeadm/kubectl/kubelet présents en PATH (via /usr/bin ou /usr/sbin).
    absent  -> pas d'exigence (les binaires peuvent ne plus exister).
    """
    v = _vars(host)
    if v["kube_state"] != "present":
        pytest.skip("Présence des binaires vérifiée seulement quand kube_state=present.")

    # On tolère que le PATH diffère selon l'image. On cherche via 'command -v'
    for bin_name in ("kubeadm", "kubectl", "kubelet"):
        cmd = host.run(f"bash -lc 'command -v {bin_name}'")
        assert cmd.rc == 0, f"{bin_name} devrait être résolvable dans le PATH (rc={cmd.rc}, err={cmd.stderr})"
