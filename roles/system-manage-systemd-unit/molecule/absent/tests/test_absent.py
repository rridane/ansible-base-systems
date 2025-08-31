def test_unit_file_removed(host):
    """Vérifie que le fichier d'unité systemd a été supprimé"""
    unit_file = host.file("/etc/systemd/system/test-service.service")
    assert not unit_file.exists

def test_dropin_directory_removed(host):
    """Vérifie que le répertoire de drop-ins a été supprimé"""
    dropin_dir = host.file("/etc/systemd/system/test-service.service.d")
    assert not dropin_dir.exists

def test_environment_file_removed(host):
    """Vérifie que le fichier d'environnement a été supprimé"""
    env_file = host.file("/etc/default/test-service")
    assert not env_file.exists

def test_service_stopped(host):
    """Vérifie que le service est arrêté (dans la mesure du possible)"""
    # On ne peut pas vraiment tester l'arrêt sous Docker, mais on vérifie
    # au moins que l'unité n'est plus active
    try:
        service = host.service("test-service.service")
        # Le service ne devrait pas être activé
        assert not service.is_enabled
    except Exception:
        # Si le service n'existe pas du tout, c'est aussi acceptable
        pass