# Ansible Role: rridane.base_systems.system_install_haproxy_keepalived

This role installs and configures **HAProxy** (L4/L7 load balancer) and **Keepalived** (VRRP for high-availability virtual IP).  
It deploys configuration files, enables the services, and checks their proper operation.  
Supports **present/absent** states.

---

## 🚀 Installation

`requirements.yml`:

```yaml
- name: rridane.base_systems.system_install_haproxy_keepalived
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

## ⚙️ Variables

| Variable                     | Default        | Description |
|------------------------------|----------------|-------------|
| haproxy_username             | haproxy        | User under which HAProxy runs |
| haproxy_groupname            | haproxy        | Group under which HAProxy runs |
| haproxy_default_mode         | tcp            | Default mode (`tcp` or `http`) |
| haproxy_frontend_stats_port  | 8404           | Listening port of the statistics frontend |
| api_server_frontend_port     | 6443           | Frontend port exposing the Kubernetes cluster (API server) |
| haproxy_extra_frontends      | []             | List of additional frontends |
| haproxy_extra_backends       | []             | List of additional backends |
| masters                      | []             | List of Kubernetes API masters (hostname, ip, port) |
| nodes                        | []             | List of nodes (hostname, ip, port) for Traefik or others |
| keepalived_interface         | eth0           | Network interface used by VRRP |
| ha_vip                       | 192.168.0.100  | High-availability virtual IP managed by Keepalived |
| keepalived_priority_master   | 101            | Priority of the master node (higher = MASTER) |
| keepalived_priority_backup   | 100            | Priority of the backup node |
| keepalived_virtual_router_id | 100            | VRRP identifier shared between nodes |

## ✅ Effects

- `haproxy` service **enabled + running**.
- `keepalived` service **enabled + running**.
- HAProxy config deployed and validated.
- API frontend accessible at `ha_vip:6443`.
- Stats frontend + Prometheus exporter available at `ha_vip:8404`.
- Floating `ha_vip` IP between MASTER/BACKUP via VRRP.

## 📝 Notes

### Molecule/Testinfra tests verify:
- HAProxy service running and enabled.
- `/etc/haproxy/haproxy.cfg` exists and is valid (`haproxy -c`).
- Admin socket `/run/haproxy/admin.sock` present.
- API/stats frontends listening on correct ports.
- Backends generated for each master/node.

### Keepalived
- Adjusts `priority` to switch between MASTER and BACKUP.

### Prometheus exporter
- Exposed via the directive `http-request use-service prometheus-exporter`.

### Full example

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
# Clean haproxy keepalived + purge configs
- hosts: lb_nodes
  become: true
  roles:
    - role: rridane.base_systems.system_install_haproxy_keepalived
      vars:
        haproxy_keepalived_state: absent
        haproxy_keepalived_purge: true
```
