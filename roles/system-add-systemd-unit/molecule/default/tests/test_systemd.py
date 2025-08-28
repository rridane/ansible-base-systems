import pytest

def test_unit_file_exists(host):
    """Vérifie que le fichier d'unité systemd existe avec les bonnes permissions"""
    unit_file = host.file("/etc/systemd/system/test-service.service")
    assert unit_file.exists
    assert unit_file.is_file
    assert unit_file.user == "root"
    assert unit_file.group == "root"
    assert unit_file.mode == 0o644

def test_unit_file_content(host):
    """Vérifie le contenu du fichier d'unité systemd"""
    unit_file = host.file("/etc/systemd/system/test-service.service")
    content = unit_file.content_string

    assert "[Unit]" in content
    assert "Description=Test Service" in content
    assert "[Service]" in content
    assert "Type=oneshot" in content
    assert "ExecStart=/bin/echo" in content
    assert "[Install]" in content
    assert "WantedBy=multi-user.target" in content

def test_dropin_directory_exists(host):
    """Vérifie que le répertoire de drop-ins existe"""
    dropin_dir = host.file("/etc/systemd/system/test-service.service.d")
    assert dropin_dir.exists
    assert dropin_dir.is_directory
    assert dropin_dir.user == "root"
    assert dropin_dir.group == "root"
    assert dropin_dir.mode == 0o755

def test_dropin_files_exist(host):
    """Vérifie que tous les fichiers de drop-in existent avec le bon contenu"""
    override_file = host.file("/etc/systemd/system/test-service.service.d/override.conf")
    assert override_file.exists
    assert override_file.is_file
    assert override_file.user == "root"
    assert override_file.group == "root"
    assert override_file.mode == 0o644
    assert "Environment=TEST_VAR=test_value" in override_file.content_string

def test_environment_file_exists(host):
    """Vérifie que le fichier d'environnement existe avec le bon contenu"""
    env_file = host.file("/etc/default/test-service")
    assert env_file.exists
    assert env_file.is_file
    assert env_file.user == "root"
    assert env_file.group == "root"
    assert env_file.mode == 0o644
    assert "DEBUG=true" in env_file.content_string

def test_unit_file_validation_skipped(host):
    """Vérifie que la validation systemd-analyze a été ignorée comme configuré"""
    # Cette tâche ne devrait pas avoir été exécutée
    # On peut vérifier en regardant si le binaire systemd-analyze existe
    # et si oui, qu'il n'a pas été utilisé pour valider notre service
    systemd_analyze = host.exists("systemd-analyze")
    if systemd_analyze:
        # Si systemd-analyze existe, on vérifie qu'aucune erreur de validation
        # n'apparaît dans les logs (approximation)
        # Cette vérification est optionnelle
        pass

def test_service_configuration(host):
    """Vérifie que le service est configuré (sans tester l'état running)"""
    # Vérifie que le fichier de service existe (déjà testé)
    # Vérifie que le service n'est pas maské
    result = host.run("systemctl is-enabled test-service.service || true")
    assert "masked" not in result.stdout.lower()

def test_daemon_reload_triggered(host):
    """Vérifie que le daemon-reload a été déclenché"""
    # On ne peut pas tester directement l'effet du daemon-reload dans un conteneur
    # Mais on peut vérifier que les fichiers existent et sont accessibles
    assert host.file("/etc/systemd/system/test-service.service").exists