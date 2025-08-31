# Ansible Collection — Base Systems & Kubernetes Toolkit

Cette collection fournit un ensemble de **rôles système** et **outils Kubernetes** destinés à Debian/Ubuntu.  
Objectif : disposer de **briques modulaires, idempotentes et testées** avec Molecule, pour assembler rapidement une infrastructure prête à l’emploi.

---

## 📦 Rôles inclus

### 🔧 Configuration système
- **system-configure-proxy**  
  Configure un proxy système (`http_proxy`, `https_proxy`, `no_proxy`) et supporte `cntlm`.
- **system-configure-swap**  
  Crée, active ou désactive un fichier de swap de manière idempotente.
- **system-configure-kernel-network-rules**  
  Charge et maintient des modules réseau (`br_netfilter`, etc.), configure `sysctl` pour Kubernetes.
- **system-manage-etc-hosts**  
  Gère `/etc/hosts` via blocs délimités Ansible (idempotent, sauvegarde activée).
- **system-manage-systemd-unit**  
  Crée, active ou supprime des unités `systemd` (supporte scope `system` et `user`).

### 🔐 Services & middlewares
- **system-manage-cntlm**  
  Compile, installe et configure CNTLM (proxy NTLMv2). Peut être couplé à `system-configure-proxy`.
- **system-install-nfs-commons**  
  Installe et configure les paquets NFS (`nfs-common`) pour le montage de volumes partagés.

### 🖥️ Container runtime
- **system-install-containerd**  
  Installe et configure `containerd` (runtime officiel pour Kubernetes).

### 🏗️ Kubernetes core
- **system-install-kube-packages**  
  Installe les paquets de base Kubernetes (`kubeadm`, `kubelet`, `kubectl`) depuis **pkgs.k8s.io** (avec gestion de version et keyrings).
- **system-install-haproxy-keepalived**  
  Déploie un HAProxy + Keepalived pour assurer une IP virtuelle haute-disponibilité (VIP) en frontal d’un cluster Kubernetes.
- **system-cleanup-kube**  
  Supprime les paquets, dépôts et fichiers liés à Kubernetes pour remettre le système à plat.

### 🛠️ Kubernetes toolbox
- **system-k8s-cli-swissknife**  
  Bundle d’outils CLI Kubernetes :
    - `kubectl` (dernière stable ou version précise, via APT pkgs.k8s.io)
    - `krew` + plugins utiles (`ctx`, `ns`, `stern`, etc.)
    - `k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`

---

## 🚀 Exemple d’utilisation

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
            version: ""       # dernière stable
          krew:
            enabled: true
            plugins: [ctx, ns, stern, oidc-login]
          helm:
            enabled: true
```
