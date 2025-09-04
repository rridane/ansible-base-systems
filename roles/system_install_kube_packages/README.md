# Ansible Role: rridane.base_systems.system_install_kube_packages

This role manages the installation or removal of **Kubernetes** packages (`kubeadm`, `kubelet`, `kubectl`) on Debian/Ubuntu.  
It uses the official `pkgs.k8s.io` repositories and supports **present/absent** states.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.base_systems.system_install_kube_packages
```

## ⚙️ Variables

| Variable     | Default   | Description |
|--------------|-----------|-------------|
| kube_state   | present   | `present` to install/setup, `absent` to purge/reset |
| kube_version | ""        | Exact version (e.g. `1.30.2-1.1`). Empty = latest available in the repo |
| kube_series  | v1.30     | Stable series (`v1.29`, `v1.30`…) used for pkgs.k8s.io |

---

## 🧩 What the role does

### present:
- Adds the repository `pkgs.k8s.io/core:/stable:/<series>/deb/`.
- Installs `kubeadm`, `kubelet`, `kubectl` (pinned version if `kube_version` defined).

### absent:
- Purges the packages.

## Example

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_kube_packages
      vars:
        kube_state: present
        kube_version: "1.30.2-1.1"
        kube_series: "v1.30"
```

```yaml
# Simple uninstallation
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_kube_packages
      vars:
        kube_state: absent
```
