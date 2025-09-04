# Ansible Role: rridane.base_systems.system_manage_cntlm

This role installs and configures **CNTLM** (NTLM/NTLMv2 proxy) from sources, but it does not create the systemd configuration. Consider using **rridane.base_systems.system_manage_systemd_unit** if that is required.  
Supports **present/absent** states.

---

## 🚀 Installation

`requirements.yml`:

```yaml
- name: rridane.base_systems.system_manage_cntlm
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

| Variable              | Default                       | Description |
|-----------------------|-------------------------------|-------------|
| cntlm_state           | present                       | `present` to install/configure, `absent` to remove |
| cntlm_version         | "0.94.0"                      | CNTLM version (if `cntlm_source_url` is empty, builds GitHub URL) |
| cntlm_source_url      | ""                            | Source tarball URL (priority if provided) |
| cntlm_source_checksum | ""                            | Checksum (e.g. sha256:…) to secure the download |
| cntlm_build_dir       | /usr/local/src/cntlm          | Build directory |
| cntlm_bin_path        | /usr/local/sbin/cntlm         | Binary installation path |
| cntlm_conf_path       | /etc/cntlm.conf               | Configuration file path |
| cntlm_username        | ""                            | NTLM username |
| cntlm_domain          | ""                            | Domain |
| cntlm_password        | ""                            | Password (**avoid**, prefer `cntlm_pass_ntlmv2` + Ansible Vault) |
| cntlm_pass_ntlmv2     | ""                            | NTLMv2 hash (**recommended**) |
| cntlm_listen_host     | ""                            | Listening host. If empty, CNTLM will use `Listen <port>` |
| cntlm_listen_port     | 3128                          | Listening port |
| cntlm_upstream_host   | 127.0.0.1                     | Upstream proxy host (corporate) |
| cntlm_upstream_port   | 3128                          | Upstream port |
| cntlm_no_proxy        | []                            | List of domains/IPs to exclude (converted into `NoProxy …` lines) |
| cntlm_extra_options   | []                            | Additional raw lines (e.g. `NTLMv2 on`) |

⚠ Provide exactly one of: **cntlm_password** or **cntlm_pass_ntlmv2** (and **cntlm_username** is required).

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_cntlm
      vars:
        cntlm_version: "0.94.0"
        cntlm_username: "john.doe"
        cntlm_domain: "ACME"
        # Prefer NTLMv2 hash with Ansible Vault:
        cntlm_pass_ntlmv2: "ABCD1234...EF"
        cntlm_upstream_host: "proxy.corp.local"
        cntlm_upstream_port: 8080
        cntlm_listen_port: 3128
        cntlm_no_proxy:
          - "localhost"
          - "127.0.0.1"
          - ".interne"
```
