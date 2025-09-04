# Ansible Role: rridane.base_systems.system_manage_systemd_unit

Ce rôle permet de gérer des unités **systemd** de manière flexible : création, suppression, drop-ins, environment files,
activation/désactivation et démarrage/redémarrage.

---

## 🚀 Utilisation

`requirements.yml` :

```yaml
- name: rridane.base_systems.system_manage_systemd_unit
  version: ">=1.0.0"
```

```
ansible-galaxy install -r requirements.yml
```

```
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_scope: "system"   # system | user
        unit_content: |
          [Unit]
          Description=My Demo App

          [Service]
          ExecStart=/usr/local/bin/myapp

          [Install]
          WantedBy=multi-user.target
        unit_enabled: true
        unit_state: started
```

### Fournir le contenu de l’unité (un seul mode)

Le rôle accepte exactement **un** des trois modes suivants :

| Variable            | Usage                                                                                             |
|---------------------|---------------------------------------------------------------------------------------------------|
| `unit_content`      | Contenu inline du unit file (idéal pour les petits services).                                     |
| `unit_template_src` | Chemin d’un template Jinja2 (ex: `my.service.j2`) situé dans `templates/` du rôle ou du playbook. |
| `unit_src_path`     | Chemin vers un fichier local prêt à copier (pas de templating).                                   |

---

#### Exemple 1 : Inline

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: myapp.service
        unit_content: |
          [Unit]
          Description=My App
          [Service]
          ExecStart=/usr/local/bin/myapp
          [Install]
          WantedBy=multi-user.target
```

#### Exemple 2 : Template

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: myapp.service
        unit_template_src: myapp.service.j2
        my_port: 8080
```

#### Exemple 3 : Fichier

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: myapp.service
        unit_src_path: files/myapp.service
```

#### Exemple 4 : Unité système minimale

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_scope: "system"
        unit_content: |
          [Unit]
          Description=My App
          After=network-online.target
          Wants=network-online.target

          [Service]
          ExecStart=/usr/local/bin/myapp
          Restart=on-failure

          [Install]
          WantedBy=multi-user.target
        unit_enabled: true
        unit_state: started
```

#### Exemple 5 : Ne pas toucher à l'état, modifier uniquement le fichier

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_content: |
          [Unit]
          Description=My App (file only)
          [Service]
          ExecStart=/usr/local/bin/myapp
          [Install]
          WantedBy=multi-user.target
        unit_state: null          # <- aucune action systemctl
        unit_enabled: true        # facultatif, ignoré si tu le souhaites
```

#### Exemple 6 : Full example - drop-in file + env_file + restart

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_content: |
          [Unit]
          Description=My App
          After=network.target
          [Service]
          EnvironmentFile=/etc/default/myapp
          ExecStart=/usr/local/bin/myapp --port ${PORT}
          [Install]
          WantedBy=multi-user.target

        unit_envfile_path: /etc/default/myapp
        unit_envfile_content: |
          PORT=8080

        unit_dropins:
          - name: override.conf
            content: |
              [Service]
              Restart=always
              RestartSec=2

        unit_restart_on_change: true
        unit_state: restarted
        unit_enabled: true
```

#### Exemple 7 : clean

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_present: false
```