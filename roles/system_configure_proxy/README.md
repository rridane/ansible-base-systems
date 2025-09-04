# Ansible Role: rridane.base_systems.system_configure_proxy

Properly configures **system proxies**:
- **APT** (`/etc/apt/apt.conf.d/99-proxy.conf`)
- **/etc/environment** (managed block, case-sensitive)
- **systemd [Manager] DefaultEnvironment** (persistent drop-in) + `daemon-reexec`

Manages **present/absent** states and automatically merges `no_proxy_list` + `no_proxy_extra` if explicit `no_proxy` is empty.

---

## 🚀 Installation

`requirements.yml`:

```yaml
- name: rridane.base_systems.system_configure_proxy
  version: ">=1.0.0"
```

```
ansible-galaxy install -r requirements.yml
```

## Variables

| Variable               | Default                                     | Description |
|------------------------|---------------------------------------------|-------------|
| proxy_state            | present                                     | `present` to create/maintain, `absent` to remove |
| http_proxy             | ""                                          | HTTP proxy URL, e.g. `http://proxy:3128` |
| https_proxy            | ""                                          | HTTPS proxy URL, falls back to `http_proxy` if empty |
| no_proxy               | ""                                          | Explicit list (priority). If not empty, used as-is |
| no_proxy_list          | ["127.0.0.1","localhost",".svc",".cluster.local"] | Base NO_PROXY if `no_proxy` is empty |
| no_proxy_extra         | []                                          | Additional elements merged (unique) to `no_proxy_list` if `no_proxy` is empty |
| apt_proxy_file         | /etc/apt/apt.conf.d/99-proxy.conf           | APT configuration file |
| environment_file       | /etc/environment                            | Global environment file |
| environment_block_name | ansible_managed_proxy                       | Managed block name (marker) in `/etc/environment` |
| systemd_dropin_dir     | /etc/systemd/system.conf.d                  | systemd [Manager] drop-in directory |
| systemd_dropin_file    | 10-proxy.conf                               | Drop-in file name |

## Concrete example

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_proxy
      vars:
        http_proxy: "http://proxy.example:3128"
        # https_proxy: ""       # ← http_proxy if empty
        no_proxy_extra:
          - ".interne"
          - "10.0.0.0/8"
```
