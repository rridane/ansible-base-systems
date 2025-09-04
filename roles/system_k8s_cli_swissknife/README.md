# Ansible Role: rridane.system-k8s-cli-swissknife

Bundle d’outils **CLI Kubernetes** (**hors kubectl**) :  
`krew` (+ plugins), `k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye` pour **Debian/Ubuntu**.

🎯 Objectif : une **boîte à outils prête à l’emploi**, idempotente, et facilement **pilotée par variables**.

---

## ✅ Compatibilité & prérequis

- **OS** : Debian 12+, Ubuntu 20.04/22.04.
- **krew** : nécessite `git`.
- **kubectl** : **non géré par ce rôle**.
  - Si `kubectl` est absent, l’installation des **plugins krew** est **sautée**.
  - krew reste installé et prêt à l’emploi une fois `kubectl` disponible.

---

## ⚙️ Variables

### Globales

- `tools_state` (`present` | `absent`)  
  État global : installer/configurer ou désinstaller.
- `bin_path` : chemin où installer les binaires (défaut `/usr/local/bin`).
- `system_arch` : architecture (`amd64` ou `arm64`).

### `tools.krew`

- `enabled` (bool, défaut `true`) – active/désactive krew.
- `version` (str, défaut `""`) – version, `""` = dernière release.
- `krew_root` (str, défaut `/opt/krew`) – racine d’installation.
- `plugins` (list) – plugins à installer via `kubectl krew` (skippés si `kubectl` absent).

### Autres outils (`k9s`, `kustomize`, `helm`, `jq`, `yq`, `kubent`, `popeye`)

- `enabled` (bool) – active/désactive l’outil.
- `version` (str) – `""` = dernière release.
- `arch` (str) – `amd64` ou `arm64` (si applicable).

---

## 🧩 Ce que le rôle fait

- **krew** :
  - Télécharge et installe le binaire.
  - Ajoute `/etc/profile.d/krew.sh` pour le PATH.
  - Installe les plugins si `kubectl` est présent, sinon affiche un avertissement.

- **Autres outils** :
  - Télécharge et installe les binaires (ou paquets pour `jq`).
  - Crée les fichiers dans `{{ bin_path }}`.

- **Désinstallation (`tools_state: absent`)** :
  - Supprime les binaires gérés (`helm`, `k9s`, `kustomize`, `kubent`, `popeye`, `yq`).
  - Désinstalle `jq` via APT.
  - Supprime `krew_root` et le script PATH (`/etc/profile.d/krew.sh`).

---

## 🚀 Exemples

👉 Mettre exemple installation ici
```yaml
# installation simple
- hosts: all
  become: true
  roles:
    - role: rridane.system-k8s-cli-swissknife
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
    - role: rridane.system-k8s-cli-swissknife
      vars:
        tools_state: absent
```

---

## ✅ Effets attendus

- Tous les binaires activés présents dans `bin_path`.
- `jq` installé via APT.
- `krew` disponible dans le PATH via `/etc/profile.d/krew.sh`.
- Plugins krew installés si `kubectl` est présent.
- En mode `absent`, tout est proprement retiré (hors kubectl).

---

## 📝 Notes

- Ce rôle **ne gère pas kubectl**.
- `jq` est géré via APT, les autres via binaires GitHub.
- Plugins krew : **idempotents** si `kubectl` est installé.
- Testé sur Debian 12 et Ubuntu 20.04/22.04.