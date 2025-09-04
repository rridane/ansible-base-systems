# Ansible Role: rridane.base_systems.etc_hosts

Ce rôle gère un **bloc Ansible-managé** dans `/etc/hosts` pour ajouter/retirer des entrées de manière **idempotente**.  
Il crée un bloc délimité par des marqueurs `# ANSIBLE-MANAGED <block_name> BEGIN/END`, y insère vos lignes, et peut le supprimer proprement.

---

## 🚀 Installation

```yaml
# requirements.yml
- name: rridane.base_systems.etc_hosts
  version: ">=1.0.0"
```

## ⚙️ Variables

| Variable             | Défaut      | Description                                                     |
|----------------------|-------------|-----------------------------------------------------------------|
| etc_hosts_state      | present     | `present` pour créer/mettre à jour le bloc, `absent` pour le supprimer |
| etc_hosts_block_name | etc-hosts   | Nom logique du bloc (utilisé dans les marqueurs BEGIN/END)      |
| etc_hosts_backup     | true        | Sauvegarder `/etc/hosts` lors des modifications                 |
| etc_hosts            | []          | Liste des entrées à écrire dans le bloc                         |

## Structure des entrées etc_hosts

```yaml
etc_hosts:
  - ip: "10.0.0.10"
    names: ["api.internal", "api"]   # alias affichés sur la même ligne
    comment: "API server"            # (optionnel) commentaire en fin de ligne
```

## 💡 Format de rendu d’une ligne
`IP  <names...> [names]  # comment`

## 🧩 Ce que le rôle fait

- Si le bloc existe déjà, il **remplace** son contenu entre les marqueurs (regex sûre).
- S’il n’existe pas, il **crée** les lignes :
  ```text
  # ANSIBLE-MANAGED <block_name> BEGIN
  ...vos entrées générées...
  # ANSIBLE-MANAGED <block_name> END
    ```
- state: absent → supprime proprement le bloc (les autres parties de /etc/hosts ne sont pas touchées).

- En environnement conteneurisé, utilise des écritures non sûres (unsafe_writes) pour pallier certaines contraintes d’overlay.

## Exemples

### Créer un bloc

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.etc_hosts
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

### Supprimer le bloc

```yaml
- hosts: all
  become: true
  roles:
    - role: rridane.base_systems.etc_hosts
      vars:
        etc_hosts_state: absent
        etc_hosts_block_name: "k8s-lab"
```

## ✅ Effets attendus

Le fichier `/etc/hosts` contient un bloc délimité par : 

```bash
ANSIBLE-MANAGED <block_name> BEGIN
ANSIBLE-MANAGED <block_name> END
```


- Toutes les lignes définies dans `etc_hosts` sont présentes **entre** ces marqueurs.
- En mode `absent`, ces deux marqueurs et le contenu intermédiaire **disparaissent**.

---

## 🧪 Tests (Molecule / Testinfra)

- `/etc/hosts` existe et est un fichier.
- Le bloc `BEGIN/END` utilisant `etc_hosts_block_name` est présent (ou absent si `state=absent`).
- Les lignes construites à partir de `etc_hosts` sont trouvées dans le bloc.
- Le rôle est **idempotent** : un second run ne produit **aucun changement**.

---

## 📝 Notes

- Le template utilisé pour les lignes est basé sur `hosts_block.j2`.
- Seul le bloc managé est modifié ; le reste de `/etc/hosts` n’est pas touché.
- `backup: true` par défaut : une sauvegarde de `/etc/hosts` est conservée avant modification.
- Les écritures utilisent `unsafe_writes` en conteneur pour éviter des erreurs d’overlay fs.




