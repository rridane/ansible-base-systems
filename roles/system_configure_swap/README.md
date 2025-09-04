# ansible role rridane.base_systems.system_configure_swap

Active ou désactive le **swap** sur un système Linux (Ubuntu/Debian).  
Le rôle agit de manière **idempotente** : il commente/décommente les entrées `swap` dans `/etc/fstab` et exécute `swapon`/`swapoff` pour appliquer immédiatement.

## Variables

| Variable       | Type  | Défaut | Description |
|----------------|-------|--------|-------------|
| `swap_enabled` | bool  | `false` | Contrôle l'état du swap. <br> - `true` → active le swap et décommente les entrées dans `/etc/fstab`. <br> - `false` → désactive le swap et commente les entrées dans `/etc/fstab`. |

## Exemple d’utilisation

```yaml
# Désactive le swap (recommandé pour kubernetes)
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_swap
      vars:
        swap_enabled: false # Désactive le swap
```

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_configure_swap
      vars:
        swap_enabled: false # Réactive le swap
```

## Notes

- Le rôle n’ajoute pas de nouveau fichier de swap. Il gère uniquement l’activation/désactivation des entrées déjà présentes dans /etc/fstab.

- Si aucun swap n’est défini, swapon -a n’aura pas d’effet.

- Testé sur Ubuntu 22.04 (Jammy).

- Compatibilité

Ansible >=2.12
Ubuntu 22.04 (Jammy)