import pytest

def test_template_based_unit_file(host):
    """Vérifie qu'une unité basée sur un template est correctement déployée"""
    unit_file = host.file("/etc/systemd/system/template-service.service")
    assert unit_file.exists
    assert unit_file.is_file
    assert unit_file.user == "root"
    assert unit_file.group == "root"

    # Vérifie le contenu spécifique au template
    # (supposant que le template contient une ligne spécifique)
    assert unit_file.contains("Description=Service from template")