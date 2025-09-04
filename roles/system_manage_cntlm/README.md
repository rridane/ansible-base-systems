# Ansible Role: rridane.base_systems.system_manage_cntlm

Ce rôle installe et configure **CNTLM** (proxy NTLM/NTLMv2) depuis les sources, mais il ne créé par la configuration systemd, envisagez l'utilisation de **rridane.base_systems.system_manage_systemd_unit** si c'est un besoin. 
Supporte les états **present/absent**.

---

## 🚀 Installation

`requirements.yml` :

```yaml
- name: rridane.base_systems.system_manage_cntlm
  version: ">=1.0.0"
```

```yaml
ansible-galaxy install -r requirements.yml
```

| Variable               | Par défaut                     | Description                                                                 |
|------------------------|---------------------------------|-----------------------------------------------------------------------------|
| cntlm_state            | present                         | `present` pour installer/configurer, `absent` pour supprimer                 |
| cntlm_version          | "0.94.0"                        | Version CNTLM (si `cntlm_source_url` est vide, construit l’URL GitHub)       |
| cntlm_source_url       | ""                              | URL du tarball source (prioritaire si renseignée)                            |
| cntlm_source_checksum  | ""                              | Checksum (ex: sha256:…) pour sécuriser le téléchargement                     |
| cntlm_build_dir        | /usr/local/src/cntlm            | Dossier de compilation                                                       |
| cntlm_bin_path         | /usr/local/sbin/cntlm           | Chemin d’installation du binaire                                             |
| cntlm_conf_path        | /etc/cntlm.conf                 | Chemin du fichier de configuration                                           |
| cntlm_username         | ""                              | Nom d’utilisateur NTLM                                                       |
| cntlm_domain           | ""                              | Domaine                                                                      |
| cntlm_password         | ""                              | Mot de passe (**évitez**, préférez `cntlm_pass_ntlmv2` + Ansible Vault)      |
| cntlm_pass_ntlmv2      | ""                              | Hash NTLMv2 (**recommandé**)                                                 |
| cntlm_listen_host      | ""                              | Hôte d’écoute. Si vide, CNTLM utilisera `Listen <port>`                      |
| cntlm_listen_port      | 3128                            | Port d’écoute                                                                |
| cntlm_upstream_host    | 127.0.0.1                       | Hôte du proxy upstream (corporate)                                           |
| cntlm_upstream_port    | 3128                            | Port upstream                                                                |
| cntlm_no_proxy         | []                              | Liste de domaines/IP à exclure (convertie en lignes `NoProxy …`)             |
| cntlm_extra_options    | []                              | Lignes additionnelles brutes (ex: `NTLMv2 on`)                               |

⚠ Fournissez exactement un des deux : **cntlm_password** ou **cntlm_pass_ntlmv2** (et **cntlm_username** requis).

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.system_manage_cntlm
      vars:
        cntlm_version: "0.94.0"
        cntlm_username: "john.doe"
        cntlm_domain: "ACME"
        # Préférez le hash NTLMv2 avec Ansible Vault :
        cntlm_pass_ntlmv2: "ABCD1234...EF"
        cntlm_upstream_host: "proxy.corp.local"
        cntlm_upstream_port: 8080
        cntlm_listen_port: 3128
        cntlm_no_proxy:
          - "localhost"
          - "127.0.0.1"
          - ".interne"
```
