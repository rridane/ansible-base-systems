# Ansible Role: rridane.system_proxy

Configure proprement les proxys **système** :
- **APT** (`/etc/apt/apt.conf.d/99-proxy.conf`)
- **/etc/environment** (bloc géré, majuscule/minuscule)
- **systemd [Manager] DefaultEnvironment** (drop-in persistant) + `daemon-reexec`

Gère les états **present/absent** et fusionne automatiquement `no_proxy_list` + `no_proxy_extra` si `no_proxy` explicite est vide.

---

## 🚀 Installation

`requirements.yml` :

```yaml
- name: rridane.system_proxy
  version: ">=1.0.0"
```

```
ansible-galaxy install -r requirements.yml
```

## Variables

| Variable               | Par défaut                                 | Description                                                                                      |
|------------------------|---------------------------------------------|--------------------------------------------------------------------------------------------------|
| proxy_state            | present                                     | `present` pour créer/maintenir, `absent` pour supprimer                                          |
| http_proxy             | ""                                          | URL HTTP proxy, ex `http://proxy:3128`                                                           |
| https_proxy            | ""                                          | URL HTTPS proxy, retombe sur `http_proxy` si vide                                                |
| no_proxy               | ""                                          | Liste explicite (prioritaire). Si non vide, utilisée telle quelle                                |
| no_proxy_list          | ["127.0.0.1","localhost",".svc",".cluster.local"] | Base de NO_PROXY si `no_proxy` est vide                                                          |
| no_proxy_extra         | []                                          | Éléments additionnels fusionnés (uniques) à `no_proxy_list` si `no_proxy` est vide               |
| apt_proxy_file         | /etc/apt/apt.conf.d/99-proxy.conf           | Fichier APT                                                                                      |
| environment_file       | /etc/environment                            | Fichier d’environnement global                                                                   |
| environment_block_name | ansible_managed_proxy                       | Nom du bloc géré (marker) dans `/etc/environment`                                                |
| systemd_dropin_dir     | /etc/systemd/system.conf.d                  | Répertoire drop-ins systemd [Manager]                                                            |
| systemd_dropin_file    | 10-proxy.conf                               | Nom du drop-in                                                                                   |

## Exemple concret

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.system_proxy
      vars:
        http_proxy: "http://proxy.example:3128"
        # https_proxy: ""       # ← http_proxy si vide
        no_proxy_extra:
          - ".interne"
          - "10.0.0.0/8"
```


