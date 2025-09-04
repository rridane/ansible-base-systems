# Ansible Role: rridane.base_systems.system_install_haproxy_keepalived

Ce rôle installe et configure **HAProxy** (load balancer L4/L7) et **Keepalived** (VRRP pour IP virtuelle haute-disponibilité).  
Il déploie les fichiers de configuration, active les services et vérifie leur bon fonctionnement.  
Supporte les états **present/absent**.

---

## 🚀 Installation

`requirements.yml` :

```yaml
- name: rridane.base_systems.system_install_haproxy_keepalived
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

## Variables

## ⚙️ Variables

| Variable                   | Par défaut     | Description                                                   |
|----------------------------|----------------|---------------------------------------------------------------|
| haproxy_username           | haproxy        | Utilisateur sous lequel tourne HAProxy                        |
| haproxy_groupname          | haproxy        | Groupe sous lequel tourne HAProxy                             |
| haproxy_default_mode       | tcp            | Mode par défaut (`tcp` ou `http`)                             |
| haproxy_frontend_stats_port| 8404           | Port d’écoute du frontend de statistiques                     |
| api_server_frontend_port   | 6443           | Port frontend exposant le cluster Kubernetes (API server)     |
| haproxy_extra_frontends    | []             | Liste de frontends supplémentaires                            |
| haproxy_extra_backends     | []             | Liste de backends supplémentaires                             |
| masters                    | []             | Liste des masters API Kubernetes (hostname, ip, port)         |
| nodes                      | []             | Liste des nodes (hostname, ip, port) pour Traefik ou autres   |
| keepalived_interface       | eth0           | Interface réseau utilisée par VRRP                            |
| ha_vip                     | 192.168.0.100  | IP virtuelle haute-dispo gérée par Keepalived                 |
| keepalived_priority_master | 101            | Priorité du nœud maître (plus haute = MASTER)                 |
| keepalived_priority_backup | 100            | Priorité du nœud backup                                       |
| keepalived_virtual_router_id | 100          | Identifiant VRRP partagé entre les nœuds                      |

## ✅ Effets

- Service `haproxy` **enabled + running**.
- Service `keepalived` **enabled + running**.
- Config HAProxy déployée et validée.
- Frontend API accessible sur `ha_vip:6443`.
- Frontend stats + Prometheus exporter disponible sur `ha_vip:8404`.
- IP virtuelle `ha_vip` flottante entre MASTER/BACKUP via VRRP.

## 📝 Notes

### Tests Molecule/Testinfra vérifient :
- HAProxy service en marche et activé.
- Fichier `/etc/haproxy/haproxy.cfg` existant et valide (`haproxy -c`).
- Présence du socket admin `/run/haproxy/admin.sock`.
- Frontends API/stats écoutent sur les bons ports.
- Backends générés pour chaque master/node.

### Keepalived
- Ajuste `priority` pour basculer entre MASTER et BACKUP.

### Prometheus exporter
- Exposé via la directive `http-request use-service prometheus-exporter`.

### Exemple complet

```yaml
- hosts: lb_nodes
  become: true
  roles:
    - role: rridane.base_systems.system_install_haproxy_keepalived
      vars:
        haproxy_username: haproxy
        haproxy_groupname: haproxy
        haproxy_default_mode: tcp
        haproxy_frontend_stats_port: 8404
        api_server_frontend_port: 6443
        masters:
          - { hostname: "master1", ip: "10.0.0.11", port: 6443 }
          - { hostname: "master2", ip: "10.0.0.12", port: 6443 }
          - { hostname: "master3", ip: "10.0.0.13", port: 6443 }
        nodes:
          - { hostname: "node1", ip: "10.0.0.21", port: 80 }
          - { hostname: "node2", ip: "10.0.0.22", port: 80 }
        keepalived_interface: eth0
        ha_vip: 10.0.0.100
        keepalived_priority_master: 101
        keepalived_priority_backup: 100
        keepalived_virtual_router_id: 100
```

```yaml
# Clean haproxy keepalived + purge des confs
- hosts: lb_nodes
  become: true
  roles:
    - role: rridane.base_systems.system_install_haproxy_keepalived
      vars:
        haproxy_keepalived_state: absent
        haproxy_keepalived_purge: true
```
