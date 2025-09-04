# Ansible Role: rridane.base_systems.system_install_nfs_commons

Ultra-simple role to **install/uninstall the NFS client**.  
On Debian/Ubuntu, installs the `nfs-common` package.

---

## 🚀 Installation

```bash
ansible-galaxy install rridane.base_systems.system_install_nfs_commons
```

| Variable          | Default  | Description |
|-------------------|----------|-------------|
| nfs_common_state  | present  | `present` to apply, `absent` to remove |

## Usage

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_nfs_commons
      vars:
        nfs_common_state: present
```

## Uninstall

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_install_nfs_commons
      vars:
        nfs_common_state: absent
```

## ✅ Expected effects

- **`nfs-common`** package installed (Debian/Ubuntu).
- Binaries present and executable:
    - `/usr/sbin/mount.nfs`
    - `/usr/sbin/showmount`

---

## 📝 Notes

- **Current target**: Debian/Ubuntu (uses `ansible.builtin.apt`).
- On **RedHat/CentOS/Rocky**, the equivalent package is **`nfs-utils`** *(not handled by this role in its minimal version)*.
- The play updates the APT index (`update_cache: true`).

---

## 🧪 Tests (Molecule / Testinfra)

- Verifies that the NFS client package is installed:
    - Debian/Ubuntu → `nfs-common`
    - EL (if later adapted) → `nfs-utils`
- Verifies that binaries exist and are executable:
    - `/usr/sbin/mount.nfs`
    - `/usr/sbin/showmount`
