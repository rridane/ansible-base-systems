# Ansible Role: rridane.base_systems.net_tuning

Ce rôle applique une configuration réseau minimale pour **Kubernetes/containers** :
- charge des **modules noyau** (ex. `overlay`, `br_netfilter`),
- applique des **sysctl** (ex. `bridge-nf-call-iptables`, `ip_forward`),
- gère les fichiers persistants `/etc/modules-load.d/*.conf` et `/etc/sysctl.d/*.conf`.

Mode **present** ⇒ applique modules + sysctl.  
Mode **absent** ⇒ retire modules + sysctl et **supprime** les fichiers `.conf`.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.base_systems.net_tuning
```

ou via **requirements.yml**:

```yaml
- name: rridane.base_systems.net_tuning
  version: ">=1.0.0"
```

## Variables 

## ⚙️ Variables

| Variable                         | Défaut                                   | Description                                                       |
|----------------------------------|-------------------------------------------|-------------------------------------------------------------------|
| net_tuning_state                 | present                                   | `present` pour appliquer, `absent` pour retirer et supprimer les `.conf` |
| net_tuning_modules               | ['overlay','br_netfilter']                | Modules noyau à charger au boot (et à chaud si autorisé)          |
| net_tuning_load_now              | true                                      | Charger les modules à chaud (désactivé auto en conteneur)         |
| net_tuning_apply_sysctl_now      | true                                      | Appliquer les sysctl immédiatement (désactivé auto en conteneur)  |
| net_tuning_sysctls               | voir ci-dessous                           | Clés sysctl à appliquer (dict `clé: valeur`)                      |
| net_tuning_modules_conf_path     | /etc/modules-load.d/net-tuning.conf       | Fichier généré pour les modules persistants                       |
| net_tuning_sysctl_conf_path      | /etc/sysctl.d/90-net-tuning.conf          | Fichier généré pour les sysctl persistants                        |

## 🧩 Ce que le rôle fait

- Installe les dépendances système nécessaires (`kmod`, `procps`/`procps-ng`) **hors conteneurs**.

### present
- Charge les modules (si `net_tuning_load_now=true`).
- Écrit `modules-load.d` avec la liste des modules.
- Applique les sysctl (si `net_tuning_apply_sysctl_now=true`) **après** le chargement des modules.
- Écrit `sysctl.d` pour la persistance.

### absent
- Retire les sysctl (*best effort*) et supprime le fichier `sysctl.d`.
- Tente de décharger les modules (*best effort*).
- Supprime le fichier `modules-load.d`.

## Installation packages simple

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.net_tuning
      vars:
        net_tuning_state: present
```

## Personnaliser modules + sysctl

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.net_tuning
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

## Nettoyage

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.net_tuning
      vars:
        net_tuning_state: absent

```

## ✅ Effets attendus

- Fichiers générés :
    - `/etc/modules-load.d/net-tuning.conf`
    - `/etc/sysctl.d/90-net-tuning.conf`
- Modules `overlay` & `br_netfilter` disponibles (chargés si autorisé).
- Sysctl appliqués **et** persistés.

---

## 📝 Notes

- Certains sysctl (ex. `net.bridge.*`) exigent **`br_netfilter`** : le rôle charge les modules **avant** d’appliquer les sysctl.
- La décharge de modules en mode `absent` est *best effort* (échoue silencieusement s’ils sont encore utilisés).
- Dépendances installées automatiquement (hors conteneurs) :
    - Debian/Ubuntu/Alpine → `kmod`, `procps`
    - RedHat/CentOS/Rocky → `kmod`, `procps-ng`
- Testé sur : Debian *bullseye/bookworm*, Ubuntu *focal/jammy/noble*.

