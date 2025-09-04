# Ansible Role: rridane.base_systems.system_cleanup_kube

**Destructive** role to clean up a Kubernetes node:
- `kubeadm reset --force` (with CRI socket),
- purge packages (`kubeadm`, `kubelet`, `kubectl`) — optional,
- remove CNI (config + interfaces) — optional,
- clean up **Calico** (config/binaries/state/iptables) — optional,
- explicit confirmation required.

---

## ⚠️ Safety

By default, the role **asks for confirmation** (`yes`) before executing destructive operations.  
In CI/non-interactive mode, disable the pause and provide the ack:

```yaml
# minimal example
kube_ask_confirmation: false
kube_cleanup_ack: "yes"
```

```yaml
# Full interactive example
# playbooks/kube_cleanup.yml
- name: Clean a Kubernetes node (interactive)
  hosts: mynode01
  become: true
  roles:
    - role: rridane.base_systems.system_cleanup_kube
      vars:
        kube_cri_socket: "/var/run/containerd/containerd.sock"
        kube_ask_confirmation: true           # will prompt yes
        kube_cleanup_enabled: true
        kube_cleanup_packages: true           # purge kubeadm/kubelet/kubectl
        kube_cleanup_cni: true                # clean /etc/cni/net.d + interfaces
        kube_cleanup_calico: true             # clean Calico best-effort
```

```yaml
# Full non-interactive example (CI) 
# playbooks/kube_cleanup.yml
- name: Clean a Kubernetes node (non-interactive)
  hosts: mynode01
  become: true
  roles:
    - role: rridane.base_systems.system_cleanup_kube
      vars:
        kube_cri_socket: "/var/run/containerd/containerd.sock"
        kube_ask_confirmation: false
        kube_cleanup_ack: "yes"
        kube_cleanup_enabled: true
        kube_cleanup_packages: true
        kube_cleanup_cni: true
        kube_cleanup_calico: true
```

```shell
ansible-playbook -i inventory/hosts playbooks/kube_cleanup.yml
```

## Variables

| Variable                  | Default                              | Description |
|---------------------------|--------------------------------------|-------------|
| kube_cleanup_enabled      | true                                 | Enables/disables the role |
| kube_cri_socket           | /var/run/containerd/containerd.sock  | CRI socket for kubeadm reset |
| kube_ask_confirmation     | true                                 | Ask for interactive confirmation |
| kube_cleanup_ack          | ""                                   | Confirmation token for CI |
| kube_cleanup_ack_expected | "yes"                                | Expected token |
| kube_cleanup_packages     | true                                 | Purge kubeadm, kubelet, kubectl |
| kube_cleanup_cni          | true                                 | Remove CNI (config + interfaces) |
| kube_cleanup_calico       | true                                 | Clean Calico (config, bins, state, iptables) |

## 🧹 Calico Cleanup Details (best effort)

- Removes: `/etc/cni/net.d/10-calico.conflist`, `/opt/cni/bin/calico*`, `/var/lib/calico`, `/var/lib/cni/networks`.
- Removes interfaces: `tunl0`, `vxlan.calico`, `cali*`.
- Flushes/deletes iptables chains `cali-*` (filter/nat/mangle).
- All cleanup tasks are **idempotent** and will not fail if items do not exist.
