# Ansible Role: rridane.base_systems.net_tuning

This role applies minimal network configuration for **Kubernetes/containers**:
- loads **kernel modules** (e.g. `overlay`, `br_netfilter`),
- applies **sysctl** (e.g. `bridge-nf-call-iptables`, `ip_forward`),
- manages persistent files `/etc/modules-load.d/*.conf` and `/etc/sysctl.d/*.conf`.

Mode **present** ⇒ applies modules + sysctl.  
Mode **absent** ⇒ removes modules + sysctl and **deletes** the `.conf` files.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.base_systems.system_configure_kernel_network_rules
```

or via **requirements.yml**:

```yaml
- name: rridane.base_systems.system_configure_kernel_network_rules
  version: ">=1.0.0" # to be checked on ansible-galaxy
```

## ⚙️ Variables

| Variable                     | Default                                | Description |
|------------------------------|----------------------------------------|-------------|
| net_tuning_state             | present                                | `present` to apply, `absent` to remove and delete `.conf` |
| net_tuning_modules           | ['overlay','br_netfilter']             | Kernel modules to load at boot (and hot-load if allowed) |
| net_tuning_load_now          | true                                   | Load modules at runtime (auto-disabled in container) |
| net_tuning_apply_sysctl_now  | true                                   | Apply sysctl immediately (auto-disabled in container) |
| net_tuning_sysctls           | see below                              | Sysctl keys to apply (dict `key: value`) |
| net_tuning_modules_conf_path | /etc/modules-load.d/net-tuning.conf    | Generated file for persistent modules |
| net_tuning_sysctl_conf_path  | /etc/sysctl.d/90-net-tuning.conf       | Generated file for persistent sysctl |

## 🧩 What the role does

- Installs required system dependencies (`kmod`, `procps`/`procps-ng`) **outside containers**.

### present

- Loads the modules (if `net_tuning_load_now=true`).
- Writes `modules-load.d` with the list of modules.
- Applies sysctl (if `net_tuning_apply_sysctl_now=true`) **after** loading modules.
- Writes `sysctl.d` for persistence.

### absent

- Removes sysctl (*best effort*) and deletes the `sysctl.d` file.
- Attempts to unload modules (*best effort*).
- Deletes the `modules-load.d` file.

## Simple package installation

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.net_tuning
      vars:
        net_tuning_state: present
```

## Customize modules + sysctl

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_kernel_network_rules
      vars:
        net_tuning_modules:
          - overlay
          - br_netfilter
          - nf_conntrack
        net_tuning_sysctls:
          net.bridge.bridge-nf-call-iptables: 1
          net.ipv4.ip_forward: 1
          net.ipv4.conf.all.rp_filter: 0
```

## Cleanup

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_kernel_network_rules
      vars:
        net_tuning_state: absent
```

## ✅ Expected effects

- Generated files:
    - `/etc/modules-load.d/net-tuning.conf`
    - `/etc/sysctl.d/90-net-tuning.conf`
- Modules `overlay` & `br_netfilter` available (loaded if allowed).
- Sysctl applied **and** persisted.

---

## 📝 Notes

- Some sysctl (e.g. `net.bridge.*`) require **`br_netfilter`**: the role loads modules **before** applying sysctl.
- Unloading modules in `absent` mode is *best effort* (silently fails if still in use).
- Dependencies automatically installed (outside containers):
    - Debian/Ubuntu/Alpine → `kmod`, `procps`
    - RedHat/CentOS/Rocky → `kmod`, `procps-ng`
- Tested on: Debian *bullseye/bookworm*, Ubuntu *focal/jammy/noble*.
