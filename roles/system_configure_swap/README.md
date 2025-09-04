# Ansible Role: rridane.base_systems.system_configure_swap

Enables or disables **swap** on a Linux system (Ubuntu/Debian).  
The role acts in an **idempotent** way: it comments/uncomments `swap` entries in `/etc/fstab` and runs `swapon`/`swapoff` to apply immediately.

## Variables

| Variable       | Type  | Default | Description |
|----------------|-------|---------|-------------|
| `swap_enabled` | bool  | `false` | Controls the swap state. <br> - `true` → enables swap and uncomments entries in `/etc/fstab`. <br> - `false` → disables swap and comments entries in `/etc/fstab`. |

## Example usage

```yaml
# Disables swap (recommended for Kubernetes)
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_swap
      vars:
        swap_enabled: false # Disable swap
```

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_swap
      vars:
        swap_enabled: true # Re-enable swap
```

## Notes

- The role does not add a new swap file. It only manages the enabling/disabling of entries already present in /etc/fstab.

- If no swap is defined, `swapon -a` will have no effect.

- Tested on Ubuntu 22.04 (Jammy).

- Compatibility:

  - Ansible >= 2.12  
  - Ubuntu 22.04 (Jammy)
