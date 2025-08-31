# Ansible Role: rridane.containerd

Ce rôle installe et configure **containerd** (service systemd, `config.toml`, registries via `hosts.toml`), gère l’activation/démarrage et optionnellement un proxy.  
Supporte les états **present/absent**.

---

## 🚀 Installation

`requirements.yml` :

```yaml
- name: rridane.containerd
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

| Variable                       | Par défaut                | Description                                                                 |
|--------------------------------|----------------------------|-----------------------------------------------------------------------------|
| containerd_state               | present                    | `present` pour installer/configurer, `absent` pour retirer                  |
| containerd_version             | ""                         | Version paquet containerd (ex: 1.7.26-1). Vide = dernière depuis le repo Docker |
| containerd_root                | /mnt/data/containerd       | Répertoire data (`root`) pour containerd                                    |
| containerd_registry_config_path| /etc/containerd/certs.d    | Dossier des configs par registry (fichiers `hosts.toml`)                    |
| containerd_registries          | []                         | Liste des registries à configurer (voir structure ci-dessous)               |
| containerd_proxy               | ""                         | URL proxy pour containerd (vide pour désactiver). Ex : `http://proxy.local:3128` |

## Structure des registries

```yaml
containerd_registries:
  - host: "10.33.1.94"
    port: 5600
    insecure: true
    endpoints: ["http://10.33.1.94:5600"]
```

## 🧩 Ce que le rôle fait

- Installe *containerd* (version pinée si `containerd_version` est défini).
- Déploie `/etc/containerd/config.toml`  
  (CRI activé, `systemd_cgroup = true`, `config_path = {{ containerd_registry_config_path }}`).
- Crée un dossier par *registry* :  
  `{{ containerd_registry_config_path }}/<host>[:<port>]/hosts.toml`  
  avec les `endpoints`, `capabilities` et `skip_verify` si `insecure`/HTTP.
- Active & démarre le service `containerd`.
- (Optionnel) Applique un proxy si `containerd_proxy` est défini.
- État *absent* : stoppe/désactive le service et nettoie la configuration.

## Exemple

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.containerd
      vars:
        containerd_state: present
        containerd_root: /mnt/data/containerd
        # containerd_version: "1.7.26-1"   # optionnel, pour pinner la version
        containerd_registries:
          - host: "10.212.22.8"
            port: 5600
            insecure: true
            endpoints: ["http://10.212.22.8:5600"]
          - host: "10.212.22.8"
            port: 5500
            insecure: true
            endpoints: ["http://10.212.22.8:5500"]
```

### Effets

- `/etc/containerd/config.toml` généré (CRI activé, `config_path` pointant sur `certs.d`).
- Deux `hosts.toml` créés sous `certs.d/<host>:<port>/`.
- Service `containerd` activé (*enabled*) et démarré (*started*).

## Exemple absent

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.containerd
      vars:
        containerd_state: absent
```

### Effets (état absent)

- Service `containerd` stoppé et désactivé.
- Fichiers de configuration supprimés (incluant les registres sous `certs.d`).
- Système propre.

## 📝 Notes

### Registries & sécurité
- `insecure: true` ou des `endpoints` en `http://` forcent `skip_verify = true` dans `hosts.toml`.
- Pour du TLS avec vérification : laisse `insecure: false` et fournis tes certificats sous  
  `{{ containerd_registry_config_path }}/<host>[:<port>]/`  
  (ex: `ca.crt`, `client.cert`, `client.key`).

### CRI & Kubernetes
- Le template active `plugins."io.containerd.grpc.v1.cri".systemd_cgroup = true`.
- Définit `sandbox_image = "registry.k8s.io/pause:3.9"`.

### Proxy
- Si `containerd_proxy` est défini, le rôle peut placer les variables d’environnement (`HTTP(S)_PROXY`, `NO_PROXY`) dans l’environnement du service (selon ton implémentation).
- Pour un proxy global système, regarde aussi le rôle `rridane.system_proxy`.  
