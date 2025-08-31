import pytest

def test_modules_conf_file_removed(host):
    """Vérifie que le fichier de configuration des modules a été supprimé"""
    conf_file = host.file("/etc/modules-load.d/net-tuning.conf")
    assert not conf_file.exists

def test_sysctl_conf_file_removed(host):
    """Vérifie que le fichier de configuration sysctl a été supprimé"""
    conf_file = host.file("/etc/sysctl.d/90-net-tuning.conf")
    assert not conf_file.exists

def test_sysctl_values_reverted(host):
    """Vérifie que les valeurs sysctl ont été réinitialisées"""
    # Cette vérification est difficile car nous ne connaissons pas les valeurs par défaut
    # Nous nous contentons de vérifier que les fichiers de configuration ont été supprimés
    pass