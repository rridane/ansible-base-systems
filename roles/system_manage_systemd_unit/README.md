# Ansible Role: rridane.base_systems.system_manage_systemd_unit

This role manages **systemd units** flexibly: creation, deletion, drop-ins, environment files,
enable/disable, and start/restart.

---

## 🚀 Usage

`requirements.yml`:

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

### Provide the unit content (only one mode)

The role accepts exactly **one** of the following three modes:

| Variable            | Usage                                                                                           |
|---------------------|-------------------------------------------------------------------------------------------------|
| `unit_content`      | Inline content of the unit file (ideal for small services).                                     |
| `unit_template_src` | Path to a Jinja2 template (e.g. `my.service.j2`) located in the role or playbook `templates/`. |
| `unit_src_path`     | Path to a local ready-to-copy file (no templating).                                            |

---

#### Example 1: Inline

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

#### Example 2: Template

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

#### Example 3: File

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: myapp.service
        unit_src_path: files/myapp.service
```

#### Example 4: Minimal system unit

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

#### Example 5: Do not touch state, only modify file

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
        unit_state: null          # <- no systemctl action
        unit_enabled: true        # optional, ignored if you want
```

#### Example 6: Full example - drop-in file + env_file + restart

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

#### Example 7: clean

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_systemd_unit
      vars:
        unit_name: "myapp.service"
        unit_present: false
```
