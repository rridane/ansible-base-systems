# system-k8s-cli-swissknife

Bundle d’outils **CLI Kubernetes** (`kubectl`, `krew` + plugins, `k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`) pour **Debian/Ubuntu**.  
Objectif : une **boîte à outils prête à l’emploi**, idempotente, et facilement **pilotée par variables**.

---

## ✅ Compatibilité & prérequis

- **OS** : Debian 12+, Ubuntu 20.04/22.04 (images Molecule supportées).
- **Accès réseau** aux dépôts officiels/releases (pkgs.k8s.io, GitHub).
- Paquets de base : `ca-certificates`, `gnupg`.
- **krew** : nécessite `git` pour cloner l’index (`krew-index`).

---

## 🚀 Ce que fait le rôle (vue d’ensemble)

### krew
- Télécharge la **release** (dernière ou version fixée), **bootstrap** krew dans `krew_root`.
- Ajoute `/etc/profile.d/krew.sh`.
- Installe la **liste de plugins** demandée (idempotent).

### Autres outils (si activés)
- `k9s`
- `kustomize`
- `helm`
- `jq`
- `yq`
- `kubent`
- `popeye`

## Variables

### Variables globales

```yaml
bin_path: "/usr/local/bin"
system_arch: "amd64"
```

```yaml
tools:
  krew:
    enabled: true
    version: ""     # "" => dernière release krew
    krew_root: "/opt/krew"
    plugins:
      - ctx
      - ns
      - neat
      - view-secret
      - who-can
      - rbac-view
      - tree
      - node-shell
      - stern
      - oidc-login
  k9s:
    enabled: true
    version: ""
    arch: "amd64"
  kustomize:
    enabled: true
    version: ""
    arch: "amd64"
  helm:
    enabled: true
    version: ""
    arch: "amd64"
  jq:
    enabled: true
    version: ""
  yq:
    enabled: true
    version: ""
    arch: "amd64"
  kubent:
    enabled: true
    version: ""
    arch: "amd64"
  popeye:
    enabled: true
    version: ""
    arch: "amd64"

```

### `tools.krew`

| Clé       | Type | Défaut    | Notes |
|-----------|------|-----------|-------|
| enabled   | bool | true      | Active/désactive. |
| version   | str  | ""        | `""` ⇒ dernière release. |
| krew_root | str  | /opt/krew | Racine d’installation. |
| plugins   | list | (voir YAML) | Plugins à installer via `kubectl-krew`. |

---

### Autres (`k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`)

| Clé     | Type | Défaut | Notes |
|---------|------|--------|-------|
| enabled | bool | true   | Active/désactive l’outil. |
| version | str  | ""     | `""` ⇒ dernière release stable (selon implémentation du rôle). |
| arch    | str  | amd64  | Si pertinent pour l’outil (binaire). |


## 🔍 Comportement détaillé

### kubectl (via APT pkgs.k8s.io)

**Résolution de version**
- `version == ""` ⇒ fetch [https://dl.k8s.io/release/stable.txt](https://dl.k8s.io/release/stable.txt) → ex. `v1.30.4`.
- Déduit la série `vX.Y` (ex. `v1.30`) pour l’URL pkgs.k8s.io.

**Dépôt & clé**
- Télécharge `Release.key`, dearmor vers `/etc/apt/keyrings/kubernetes-archive-keyring.gpg` (en `0644`).
- Ajoute le dépôt :
  ```text
  deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://pkgs.k8s.io/core:/stable:/vX.Y/deb/ /
  ```
- Si une version précise a été résolue (ex. v1.30.4), le rôle tente de pinner via la version APT exacte (ex. 1.30.4-1.1) résolue par apt-cache madison.
- Sinon, installe la dernière disponible dans la série.

💡 Astuce : en cas d’absence de correspondance APT exacte, le rôle retombe proprement sur l’installation sans pin (dernière de la série).

### krew

- Récupère la **dernière version** (ou celle demandée) depuis GitHub.
- **Bootstrap** krew via le binaire krew-linux_<arch> (nécessite git installé).
- Crée /etc/profile.d/krew.sh pour exposer {{ krew_root }}/bin dans le PATH.
- Installe les **plugins listés** si non présents (**idempotent**).

## Exemples

```yaml
tools:
  kubectl:
    enabled: true
    version: ""      # => dernière stable
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
    enabled: false
  helm:
    enabled: false
```

```yaml
tools:
  kubectl:
    enabled: true
    version: "v1.30.3"   # le rôle résoudra la version APT exacte
  krew:
    enabled: true
    version: ""
    krew_root: "/opt/krew"
    plugins: [ "neat", "view-secret", "who-can" ]
  k9s:
    enabled: true
    version: "0.32.5"
  helm:
    enabled: true
    version: "3.13.3"

```