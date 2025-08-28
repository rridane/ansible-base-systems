import re
import logging
log = logging.getLogger(__name__)

def test_k9s_binary_exists_and_mode(host):

    bin_path = "/usr/local/bin/k9s"
    f = host.file(bin_path)
    assert f.exists, f"{bin_path} should exist"
    assert f.is_file, f"{bin_path} should be a file"
    assert f.mode & 0o111, f"{bin_path} should be executable"

def test_k9s_version(host):
    """
    La version attendue est celle donnée à Molecule via env K9S_VERSION
    ou la valeur par défaut du converge.yml (0.32.5).
    On lit la variable d'env dans le conteneur via `echo` pour éviter
    de la dupliquer dans le test.
    """
    expected = host.ansible.get_variables().get('k9s_version', '0.50.9')

    cmd = host.run("/usr/local/bin/k9s version --short | grep Version | awk '{print $2}'")
    assert cmd.rc == 0, f"Command failed: {cmd.stderr}"
    version = cmd.stdout.strip()
    version = re.sub(r'^v', '', version)
    assert version == expected, f"k9s version '{version}' != expected '{expected}'"
