# Ansible Role: rridane.kube_packages

Ce rôle gère l’installation ou la purge des paquets **Kubernetes** (`kubeadm`, `kubelet`, `kubectl`) sur Debian/Ubuntu.  
Il utilise les dépôts officiels `pkgs.k8s.io` et prend en charge l’état **present/absent**.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.kube_packages
```

## ⚙️ Variables

| Variable        | Par défaut                          | Description                                                                 |
|-----------------|--------------------------------------|-----------------------------------------------------------------------------|
| kube_state      | present                             | `present` pour installer/mettre en place, `absent` pour purger/réinitialiser |
| kube_version    | ""                                  | Version exacte (ex: `1.30.2-1.1`). Vide = dernière version dispo dans le repo |
| kube_series     | v1.30                               | Série stable (`v1.29`, `v1.30`…) utilisée pour pkgs.k8s.io                   |
| kube_cri_socket | /var/run/containerd/containerd.sock | Socket CRI passé à `kubeadm reset` (containerd ou CRI-O)                     |

---

## 🧩 Ce que le rôle fait

### present :
- Ajoute le dépôt `pkgs.k8s.io/core:/stable:/<series>/deb/`.
- Installe `kubeadm`, `kubelet`, `kubectl` (version pinée si `kube_version` défini).

### absent :
- Purge les paquets.

## Exemple

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.kube_packages
      vars:
        kube_state: present
        kube_version: "1.30.2-1.1"
        kube_series: "v1.30"
```

