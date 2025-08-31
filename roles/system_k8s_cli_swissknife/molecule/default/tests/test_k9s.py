import re
import logging
import pytest

log = logging.getLogger(__name__)

# Test générique pour vérifier la présence et l'exécutabilité d'un binaire
def test_binary_exists_and_executable(host, binary_path):
    f = host.file(binary_path)
    assert f.exists, f"{binary_path} should exist"
    assert f.is_file, f"{binary_path} should be a file"
    assert f.mode & 0o111, f"{binary_path} should be executable"

# Test pour vérifier la version d'un outil (si applicable)
def test_tool_version(host, tool_cmd, expected_version):
    cmd = host.run(tool_cmd)
    assert cmd.rc == 0, f"Command failed: {cmd.stderr}"

    # Extraction de la version de la sortie (adaptée à chaque outil)
    version_match = re.search(r'(\d+\.\d+\.\d+)', cmd.stdout)
    if version_match:
        version = version_match.group(1)
        assert version == expected_version, f"Tool version '{version}' != expected '{expected_version}'"

# Tests spécifiques pour chaque outil
def test_kubectl_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/kubectl")

def test_kubectl_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('kubectl', {}).get('version', '')
    if expected:  # Only test version if explicitly specified
        test_tool_version(host, "/usr/local/bin/kubectl version --client --short", expected)

def test_k9s_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/k9s")

def test_k9s_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('k9s', {}).get('version', '')
    if expected:
        cmd = host.run("/usr/local/bin/k9s version --short | grep Version | awk '{print $2}'")
        assert cmd.rc == 0, f"Command failed: {cmd.stderr}"
        version = cmd.stdout.strip()
        version = re.sub(r'^v', '', version)
        assert version == expected, f"k9s version '{version}' != expected '{expected}'"

def test_krew_exists(host):
    test_binary_exists_and_executable(host, "/opt/krew/bin/kubectl-krew")

def test_krew_plugins_installed(host):
    plugins = host.ansible.get_variables().get('tools', {}).get('krew', {}).get('plugins', [])
    for plugin in plugins:
        cmd = host.run("/opt/krew/bin/kubectl-krew list | grep " + plugin)
        assert cmd.rc == 0, f"Krew plugin {plugin} is not installed"

def test_kustomize_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/kustomize")

def test_kustomize_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('kustomize', {}).get('version', '')
    if expected:
        test_tool_version(host, "/usr/local/bin/kustomize version --short", expected)

def test_helm_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/helm")

def test_helm_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('helm', {}).get('version', '')
    if expected:
        test_tool_version(host, "/usr/local/bin/helm version --short", expected)

def test_jq_exists(host):
    # jq est généralement installé via le gestionnaire de paquets
    cmd = host.run("which jq")
    assert cmd.rc == 0, "jq is not installed"

def test_yq_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/yq")

def test_yq_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('yq', {}).get('version', '')
    if expected:
        test_tool_version(host, "/usr/local/bin/yq --version", expected)

def test_kubent_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/kubent")

def test_kubent_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('kubent', {}).get('version', '')
    if expected:
        test_tool_version(host, "/usr/local/bin/kubent --version", expected)

def test_popeye_exists(host):
    test_binary_exists_and_executable(host, "/usr/local/bin/popeye")

def test_popeye_version(host):
    expected = host.ansible.get_variables().get('tools', {}).get('popeye', {}).get('version', '')
    if expected:
        test_tool_version(host, "/usr/local/bin/popeye version", expected)
