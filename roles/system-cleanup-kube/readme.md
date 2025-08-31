# Ansible Role: rridane.base_systems.kube_cleanup

Rôle **destructif** pour nettoyer un nœud Kubernetes :
- `kubeadm reset --force` (avec socket CRI),
- purge des paquets (`kubeadm`, `kubelet`, `kubectl`) — optionnel,
- suppression CNI (conf + interfaces) — optionnel,
- nettoyage **Calico** (conf/binaires/état/iptables) — optionnel,
- confirmation explicite requise.

---

## ⚠️ Sécurité

Par défaut, le rôle **demande confirmation** (`yes`) avant d’exécuter les opérations destructives.  
En CI/non-interactif, désactive la pause et fournis l’ack :

```yaml
kube_ask_confirmation: false
kube_cleanup_ack: "yes"
```

| Variable               | Défaut                                 | Description                                      |
|------------------------|----------------------------------------|--------------------------------------------------|
| kube_cleanup_enabled   | true                                   | Active/désactive le rôle                         |
| kube_cri_socket        | /var/run/containerd/containerd.sock    | Socket CRI pour kubeadm reset                    |
| kube_ask_confirmation  | true                                   | Demander la confirmation interactive             |
| kube_cleanup_ack       | ""                                     | Token de confirmation pour CI                    |
| kube_cleanup_ack_expected | "yes"                               | Token attendu                                    |
| kube_cleanup_packages  | true                                   | Purge kubeadm, kubelet, kubectl                  |
| kube_cleanup_cni       | true                                   | Supprime CNI (conf + interfaces)                 |
| kube_cleanup_calico    | true                                   | Nettoie Calico (conf, bins, état, iptables)      |

## 🧹 Détails du nettoyage Calico (best effort)

- Supprime : `/etc/cni/net.d/10-calico.conflist`, `/opt/cni/bin/calico*`, `/var/lib/calico`, `/var/lib/cni/networks`.
- Supprime interfaces : `tunl0`, `vxlan.calico`, `cali*`.
- Vide/supprime chaînes iptables `cali-*` (filter/nat/mangle).
- Tous les nettoyages sont **idempotents** et n’échouent pas si les éléments n’existent pas.
