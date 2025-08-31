# Ansible Role: rridane.nfs_common

Rôle ultra-simple pour **installer/désinstaller le client NFS**.  
Sur Debian/Ubuntu, installe le paquet `nfs-common`.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.nfs_common
```

| Variable                         | Défaut                                   | Description                                                       |
|----------------------------------|-------------------------------------------|-------------------------------------------------------------------|
| nfs_common_state | present                                   | `present` pour appliquer, `absent` pour retirer |


## Utilisation

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.nfs_common
      vars:
        nfs_common_state: present
```

## Désinstaller

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.nfs_common
      vars:
        nfs_common_state: absent

```

## ✅ Effets attendus

- Paquet **`nfs-common`** installé (Debian/Ubuntu).
- Binaries présents et exécutables :
    - `/usr/sbin/mount.nfs`
    - `/usr/sbin/showmount`

---

## 📝 Notes

- **Cible actuelle** : Debian/Ubuntu (utilise `ansible.builtin.apt`).
- Sur **RedHat/CentOS/Rocky**, le paquet équivalent est **`nfs-utils`** *(non géré par ce rôle dans sa version minimale)*.
- Le play met à jour l’index APT (`update_cache: true`).

---

## 🧪 Tests (Molecule / Testinfra)

- Vérifie que le paquet NFS client est installé :
    - Debian/Ubuntu → `nfs-common`
    - EL (si adapté ultérieurement) → `nfs-utils`
- Vérifie que les binaries existent et sont exécutables :
    - `/usr/sbin/mount.nfs`
    - `/usr/sbin/showmount`
