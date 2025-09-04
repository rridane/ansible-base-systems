# Ansible Collection — Base Systems & Kubernetes Toolkit

This collection provides a set of **system roles** and **Kubernetes tools** intended for Debian/Ubuntu.  
Goal: to have **modular, idempotent, and Molecule-tested building blocks** to quickly assemble a ready-to-use infrastructure.

---

## 📦 Included Roles

### 🔧 System configuration
- **system-configure-proxy**  
  Configures a system proxy (`http_proxy`, `https_proxy`, `no_proxy`) and supports `cntlm`.
- **system-configure-swap**  
  Creates, enables, or disables a swap file in an idempotent way.
- **system-configure-kernel-network-rules**  
  Loads and maintains network modules (`br_netfilter`, etc.), configures `sysctl` for Kubernetes.
- **system-manage-etc-hosts**  
  Manages `/etc/hosts` via Ansible-delimited blocks (idempotent, backup enabled).
- **system-manage-systemd-unit**  
  Creates, enables, or removes `systemd` units (supports `system` and `user` scope).

### 🔐 Services & middlewares
- **system-manage-cntlm**  
  Compiles, installs, and configures CNTLM (NTLMv2 proxy). Can be coupled with `system-configure-proxy`.
- **system-install-nfs-commons**  
  Installs and configures NFS packages (`nfs-common`) for mounting shared volumes.

### 🖥️ Container runtime
- **system-install-containerd**  
  Installs and configures `containerd` (official runtime for Kubernetes).

### 🏗️ Kubernetes core
- **system-install-kube-packages**  
  Installs core Kubernetes packages (`kubeadm`, `kubelet`, `kubectl`) from **pkgs.k8s.io** (with version management and keyrings).
- **system-install-haproxy-keepalived**  
  Deploys HAProxy + Keepalived to ensure a high-availability virtual IP (VIP) in front of a Kubernetes cluster.
- **system-cleanup-kube**  
  Removes packages, repositories, and files related to Kubernetes to reset the system.

### 🛠️ Kubernetes toolbox
- **system-k8s-cli-swissknife**  
  Bundle of Kubernetes CLI tools:
    - `kubectl` (latest stable or specific version, via APT pkgs.k8s.io)
    - `krew` + useful plugins (`ctx`, `ns`, `stern`, etc.)
    - `k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`

---

## 🚀 Example usage

```yaml
- hosts: all
  roles:
    - role: rridane.base_systems.system_configure_proxy
      vars:
        proxy_host: "http://proxy.local:3128"
        no_proxy: "localhost,127.0.0.1,.svc"

    - role: rridane.base_systems.system_install_containerd

    - role: rridane.base_systems.system_install_kube_packages
      vars:
        kube_state: present
        kube_version: "v1.30.3"

    - role: rridane.base_systems.system_k8s_cli_swissknife
      vars:
        tools:
          kubectl:
            enabled: true
            version: ""       # latest stable
          krew:
            enabled: true
            plugins: [ctx, ns, stern, oidc-login]
          helm:
            enabled: true
```
