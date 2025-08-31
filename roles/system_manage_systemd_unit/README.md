# Ansible Role: systemd-unit

Ce rôle permet de gérer des unités **systemd** de manière flexible : création, suppression, drop-ins, environment files,
activation/désactivation et démarrage/redémarrage.

---

## 🚀 Utilisation

`requirements.yml` :

```yaml
- name: rridane.systemd_unit
  version: ">=1.0.0"
```

```
ansible-galaxy install -r requirements.yml
```

```
- hosts: all
  become: true
  roles:
    - role: rridane.systemd_unit
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
    - role: rridane.systemd_unit
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
    - role: rridane.systemd_unit
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
    - role: rridane.systemd_unit
      vars:
        unit_name: myapp.service
        unit_src_path: files/myapp.service
```
