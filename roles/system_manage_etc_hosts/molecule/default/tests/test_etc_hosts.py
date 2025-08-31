import re
import pytest


def _markers(block_name: str):
    """
    Reconstitue les marqueurs générés par blockinfile avec {mark} = BEGIN/END.
    """
    start = f"# ANSIBLE-MANAGED {block_name} BEGIN"
    end = f"# ANSIBLE-MANAGED {block_name} END"
    return start, end


def _extract_managed_block(content: str, block_name: str):
    """
    Extrait le contenu du bloc géré entre les marqueurs BEGIN/END (sans les lignes de marqueurs).
    Retourne None si le bloc n'est pas trouvé.
    """
    start, end = _markers(block_name)
    pattern = re.compile(
        rf"{re.escape(start)}\n(.*?){re.escape(end)}",
        flags=re.DOTALL,
    )
    m = pattern.search(content)
    if not m:
        return None
    # strip final newline artifacts for simpler contains checks
    return m.group(1).strip("\n")


def test_hosts_file_exists(host):
    f = host.file("/etc/hosts")
    assert f.exists, "/etc/hosts doit exister"
    assert f.is_file, "/etc/hosts doit être un fichier"
    assert f.user in ("root", "systemd-resolve", "sysroot", "admin", "daemon")


def test_managed_block_presence_and_lines(host):
    """
    - Si etc_hosts_state == 'absent' : on vérifie que le bloc n'est pas présent.
    - Sinon : on vérifie la présence des marqueurs et de chaque ligne attendue.
    """
    vars = host.ansible.get_variables()

    # Variables du rôle avec valeurs par défaut raisonnables
    etc_hosts = vars.get("etc_hosts", []) or []
    block_name = vars.get("etc_hosts_block_name", "etc-hosts")
    state = (vars.get("etc_hosts_state") or "present").strip().lower()

    content = host.file("/etc/hosts").content_string
    start_marker, end_marker = _markers(block_name)

    print(content)

    if state == "absent":
        assert start_marker not in content, (
            f"Le bloc BEGIN '{start_marker}' ne devrait pas être présent quand state=absent"
        )
        assert end_marker not in content, (
            f"Le bloc END '{end_marker}' ne devrait pas être présent quand state=absent"
        )
        return

    # state == present (par défaut)
    assert start_marker in content, f"Marqueur BEGIN manquant : {start_marker}"
    assert end_marker in content, f"Marqueur END manquant : {end_marker}"

    block = _extract_managed_block(content, block_name)
    assert block is not None and block.strip() != "", "Le bloc géré est introuvable ou vide"

    for h in etc_hosts:
        ip = h.get("ip")
        # aliases = names + [hostname si défini] puis unique et joint par espaces
        names = h.get("names") or []
        hostname = h.get("hostname")
        aliases = list(dict.fromkeys((names + ([hostname] if hostname else []))))
        base_line = f"{ip}  {' '.join(aliases)}"

        comment = h.get("comment")
        if comment is not None and str(comment).strip() != "":
            expected_line = f"{base_line}  # {comment}"
        else:
            expected_line = base_line

        # On vérifie que la ligne attendue apparaît telle quelle dans le bloc.
        # On tolère d'éventuels espaces finaux.
        expected_pattern = re.compile(rf"^{re.escape(expected_line)}\s*$", re.MULTILINE)
        assert expected_pattern.search(block), (
            f"Ligne attendue absente du bloc géré :\n  {expected_line}\n\nBloc actuel:\n{block}"
        )


@pytest.mark.parametrize("marker_kind", ["BEGIN", "END"])
def test_markers_format(host, marker_kind):
    """
    Vérifie que le format des marqueurs correspond bien à
    '# ANSIBLE-MANAGED <name> BEGIN/END'
    quand state=present.
    """
    vars = host.ansible.get_variables()
    block_name = vars.get("etc_hosts_block_name", "etc-hosts")
    state = (vars.get("etc_hosts_state") or "present").strip().lower()
    if state == "absent":
        pytest.skip("Bloc absent : pas de marqueurs attendus")

    expected = f"# ANSIBLE-MANAGED {block_name} {marker_kind}"
    content = host.file("/etc/hosts").content_string
    assert expected in content, f"Marqueur attendu manquant : {expected}"
