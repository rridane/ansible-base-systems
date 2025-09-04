# Ansible Role: rridane.base_systems.system_manage_etc_hosts

This role manages an **Ansible-managed block** in `/etc/hosts` to add/remove entries in an **idempotent** way.  
It creates a block delimited by markers `# ANSIBLE-MANAGED <block_name> BEGIN/END`, inserts your lines, and can remove it cleanly.

---

## 🚀 Installation

```yaml
# requirements.yml
- name: rridane.base_systems.system_manage_etc_hosts
  version: ">=1.0.0"
```

## ⚙️ Variables

| Variable             | Default     | Description |
|----------------------|-------------|-------------|
| etc_hosts_state      | present     | `present` to create/update the block, `absent` to remove it |
| etc_hosts_block_name | etc-hosts   | Logical block name (used in BEGIN/END markers) |
| etc_hosts_backup     | true        | Backup `/etc/hosts` when modified |
| etc_hosts            | []          | List of entries to write in the block |

## Structure of etc_hosts entries

```yaml
etc_hosts:
  - ip: "10.0.0.10"
    names: ["api.internal", "api"]   # aliases shown on the same line
    comment: "API server"            # (optional) comment at the end of the line
```

## 💡 Render format of a line
`IP  <names...> [names]  # comment`

## 🧩 What the role does

- If the block already exists, it **replaces** its content between markers (safe regex).
- If it does not exist, it **creates** the lines:
  ```text
  # ANSIBLE-MANAGED <block_name> BEGIN
  ...your generated entries...
  # ANSIBLE-MANAGED <block_name> END
  ```
- state: absent → cleanly removes the block (other parts of /etc/hosts are not touched).

- In containerized environments, uses unsafe writes to bypass some overlay constraints.

## Examples

### Create a block

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_etc_hosts
      vars:
        etc_hosts_state: present
        etc_hosts_block_name: "k8s-lab"
        etc_hosts:
          - ip: "10.0.0.10"
            names: ["api.internal", "api"]
            comment: "API server"
          - ip: "10.0.0.20"
            names: ["traefik.internal", "traefik"]
            comment: "Ingress"
```

```ini
# ANSIBLE-MANAGED k8s-lab BEGIN
10.0.0.10  api.internal api api-01  # API server
10.0.0.20  traefik.internal traefik ing-01  # Ingress
# ANSIBLE-MANAGED k8s-lab END
```

### Remove the block

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_etc_hosts
      vars:
        etc_hosts_state: absent
        etc_hosts_block_name: "k8s-lab"
```

## ✅ Expected effects

The `/etc/hosts` file contains a block delimited by: 

```bash
ANSIBLE-MANAGED <block_name> BEGIN
ANSIBLE-MANAGED <block_name> END
```

- All lines defined in `etc_hosts` are present **between** these markers.
- In `absent` mode, these two markers and the intermediate content **disappear**.

---

## 🧪 Tests (Molecule / Testinfra)

- `/etc/hosts` exists and is a file.
- The `BEGIN/END` block using `etc_hosts_block_name` is present (or absent if `state=absent`).
- The lines built from `etc_hosts` are found in the block.
- The role is **idempotent**: a second run produces **no change**.

---

## 📝 Notes

- The template used for lines is based on `hosts_block.j2`.
- Only the managed block is modified; the rest of `/etc/hosts` is untouched.
- `backup: true` by default: a backup of `/etc/hosts` is kept before modification.
- Writes use `unsafe_writes` in container environments to avoid overlay fs errors.
