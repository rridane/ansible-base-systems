# Ansible Role: rridane.base_systems.system_k8s_cli_swissknife

Bundle of **Kubernetes CLI tools** (**excluding kubectl**):  
`krew` (+ plugins), `k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye` for **Debian/Ubuntu**.

🎯 Goal: a **ready-to-use toolbox**, idempotent, and easily **driven by variables**.

---

## ✅ Compatibility & prerequisites

- **OS**: Debian 12+, Ubuntu 20.04/22.04.
- **krew**: requires `git`.
- **kubectl**: **not managed by this role**.
  - If `kubectl` is absent, installation of **krew plugins** is **skipped**.
  - krew remains installed and ready once `kubectl` is available.

---

## ⚙️ Variables

### Global

- `tools_state` (`present` | `absent`)  
  Global state: install/configure or uninstall.
- `bin_path`: path where to install binaries (default `/usr/local/bin`).
- `system_arch`: architecture (`amd64` or `arm64`).

### `tools.krew`

- `enabled` (bool, default `true`) – enable/disable krew.
- `version` (str, default `""`) – version, `""` = latest release.
- `krew_root` (str, default `/opt/krew`) – installation root.
- `plugins` (list) – plugins to install via `kubectl krew` (skipped if `kubectl` absent).

### Other tools (`k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`)

- `enabled` (bool) – enable/disable the tool.
- `version` (str) – `""` = latest release.
- `arch` (str) – `amd64` or `arm64` (if applicable).

---

## 🧩 What the role does

- **krew**:
  - Downloads and installs the binary.
  - Adds `/etc/profile.d/krew.sh` to PATH.
  - Installs plugins if `kubectl` is present, otherwise prints a warning.

- **Other tools**:
  - Downloads and installs binaries (or packages for `jq`).
  - Places the files into `{{ bin_path }}`.

- **Uninstallation (`tools_state: absent`)**:
  - Removes managed binaries (`helm`, `k9s`, `kustomize`, `kubent`, `popeye`, `yq`).
  - Uninstalls `jq` via APT.
  - Removes `krew_root` and PATH script (`/etc/profile.d/krew.sh`).

---

## 🚀 Examples

```yaml
# simple installation
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_k8s_cli_swissknife
      vars:
        tools_state: present
        tools:
          krew:
            enabled: true
            version: ""
            krew_root: "/opt/krew"
            plugins:
              - ctx
              - ns
              - stern
              - oidc-login
          k9s:
            enabled: true
            version: "0.32.5"
          helm:
            enabled: true
            version: "3.13.3"
          jq:
            enabled: true
          yq:
            enabled: false
```

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_k8s_cli_swissknife
      vars:
        tools_state: absent
```

---

## ✅ Expected effects

- All enabled binaries present in `bin_path`.
- `jq` installed via APT.
- `krew` available in PATH via `/etc/profile.d/krew.sh`.
- krew plugins installed if `kubectl` is present.
- In `absent` mode, everything is cleanly removed (excluding kubectl).

---

## 📝 Notes

- This role **does not manage kubectl**.
- `jq` is managed via APT, others via GitHub binaries.
- krew plugins: **idempotent** if `kubectl` is installed.
- Tested on Debian 12 and Ubuntu 20.04/22.04.
