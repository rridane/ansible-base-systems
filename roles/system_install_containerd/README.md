# Ansible Role: rridane.base_systems.system_install_containerd

This role installs and configures **containerd** (systemd service, `config.toml`, registries via `hosts.toml`), manages activation/startup and optionally a proxy.  
Supports **present/absent** states.

---

## 🚀 Installation

`requirements.yml`:

```yaml
- name: rridane.base_systems.system_install_containerd
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

| Variable                        | Default                    | Description |
|---------------------------------|----------------------------|-------------|
| containerd_state                | present                    | `present` to install/configure, `absent` to remove |
| containerd_version              | ""                         | Package version of containerd (e.g. 1.7.26-1). Empty = latest from Docker repo |
| containerd_root                 | /mnt/data/containerd       | Data directory (`root`) for containerd |
| containerd_registry_config_path | /etc/containerd/certs.d    | Directory of registry configs (`hosts.toml` files) |
| containerd_registries           | []                         | List of registries to configure (see structure below) |
| containerd_proxy                | ""                         | Proxy URL for containerd (empty to disable). Ex: `http://proxy.local:3128` |

## Registry structure

```yaml
containerd_registries:
  - host: "10.33.1.94"
    port: 5600
    insecure: true
    endpoints: ["http://10.33.1.94:5600"]
```

## 🧩 What the role does

- Installs *containerd* (pinned version if `containerd_version` is defined).
- Deploys `/etc/containerd/config.toml`  
  (CRI enabled, `systemd_cgroup = true`, `config_path = {{ containerd_registry_config_path }}`).
- Creates a folder per *registry*:  
  `{{ containerd_registry_config_path }}/<host>[:<port>]/hosts.toml`  
  with `endpoints`, `capabilities`, and `skip_verify` if `insecure`/HTTP.
- Enables & starts the `containerd` service.
- (Optional) Applies a proxy if `containerd_proxy` is defined.
- *Absent* state: stops/disables the service and cleans up configuration.

## Example

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_containerd
      vars:
        containerd_state: present
        containerd_root: /mnt/data/containerd
        # containerd_version: "1.7.26-1"   # optional, to pin version
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

### Effects

- `/etc/containerd/config.toml` generated (CRI enabled, `config_path` pointing to `certs.d`).
- Two `hosts.toml` created under `certs.d/<host>:<port>/`.
- `containerd` service enabled and started.

## Example absent

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_containerd
      vars:
        containerd_state: absent
```

### Effects (absent state)

- `containerd` service stopped and disabled.
- Configuration files removed (including registries under `certs.d`).
- Clean system.

## 📝 Notes

### Registries & security
- `insecure: true` or `http://` endpoints force `skip_verify = true` in `hosts.toml`.
- For TLS with verification: leave `insecure: false` and provide your certificates under  
  `{{ containerd_registry_config_path }}/<host>[:<port>]/`  
  (e.g. `ca.crt`, `client.cert`, `client.key`).

### CRI & Kubernetes
- The template enables `plugins."io.containerd.grpc.v1.cri".systemd_cgroup = true`.
- Defines `sandbox_image = "registry.k8s.io/pause:3.9"`.

### Proxy
- If `containerd_proxy` is defined, the role can place environment variables (`HTTP(S)_PROXY`, `NO_PROXY`) into the service environment (depending on your implementation).
- For a global system proxy, also check the role `rridane.system_proxy`.
