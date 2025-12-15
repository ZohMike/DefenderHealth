# 📝 Modifications Apportées - Prime LSP et Assistance Psychologique

## 🎯 Objectif
Permettre à l'utilisateur de saisir manuellement les montants des **Prime LSP** et **Prime Assistance Psychologique** dans les cas où il doit entrer les détails des primes (Barème spécial et Forçage manuel).

---

## ✅ Modifications Effectuées

### 1️⃣ **Fichier `calculations.py`**

#### Modification de la fonction `calculer_prime_particuliers`

**Nouveaux paramètres ajoutés :**
```python
def calculer_prime_particuliers(
    # ... paramètres existants ...
    prime_lsp_manuelle: Optional[float] = None,
    prime_assist_psy_manuelle: Optional[float] = None
) -> Dict[str, Any]:
```

**Logique de calcul mise à jour :**
```python
# Utiliser les valeurs manuelles pour LSP et Assistance Psy
prime_lsp_finale = prime_lsp_manuelle if prime_lsp_manuelle is not None else 20000
prime_assist_psy_finale = prime_assist_psy_manuelle if prime_assist_psy_manuelle is not None else 35000

# Calcul final avec les valeurs manuelles
resultat = calculer_prime_avec_parametres(
    prime_nette_base=prime_nette_ajustee,
    accessoires=accessoires_finaux,
    prime_lsp=prime_lsp_finale,
    prime_assist_psy=prime_assist_psy_finale,
    # ...
)
```

---

### 2️⃣ **Fichier `santecotation.py`**

#### A. Section Barème Spécial Particuliers (lignes ~2200-2240)

**Ajout de 2 champs de saisie :**

```python
col_man3, col_man4 = st.columns(2)

prime_lsp_manuelle = col_man3.number_input(
    "Prime LSP (FCFA)",
    min_value=0.0,
    value=20000.0,
    step=1000.0,
    key=f"prime_lsp_manuel_{bareme_key}",
    help="Prime Lettre de Sortie Provisoire"
)

prime_assist_psy_manuelle = col_man4.number_input(
    "Prime Assistance Psychologique (FCFA)",
    min_value=0.0,
    value=35000.0,
    step=1000.0,
    key=f"prime_assist_psy_manuel_{bareme_key}",
    help="Prime d'assistance psychologique"
)
```

**Stockage des valeurs :**
```python
st.session_state.baremes_speciaux_info[bareme_key] = {
    'plafond_personne': plafond_personne,
    'plafond_famille': plafond_famille,
    'taux_couverture': taux_couverture,
    'prime_lsp': prime_lsp_manuelle,
    'prime_assist_psy': prime_assist_psy_manuelle
}
```

**Passage des valeurs à la fonction de calcul :**
```python
# Récupérer les primes LSP et Assistance Psy pour barème spécial
prime_lsp_man = None
prime_assist_psy_man = None
if bareme_key == 'bareme_special':
    bareme_info = st.session_state.baremes_speciaux_info.get(bareme_key, {})
    prime_lsp_man = bareme_info.get('prime_lsp')
    prime_assist_psy_man = bareme_info.get('prime_assist_psy')

resultat = calculer_prime_particuliers(
    # ... autres paramètres ...
    prime_lsp_manuelle=prime_lsp_man,
    prime_assist_psy_manuelle=prime_assist_psy_man
)
```

#### B. Section Forçage Manuel Corporate Excel (lignes ~3365-3480)

**Ajout de 2 champs de saisie pour le forçage :**

```python
col_force3, col_force4 = st.columns(2)

with col_force3:
    prime_lsp_forcee = st.number_input(
        "Prime LSP Totale Forcée (FCFA)",
        min_value=0.0,
        value=float(services_originaux / 2),
        step=1000.0,
        key="prime_lsp_forcee_corp",
        help="Prime LSP totale pour tous les assurés"
    )

with col_force4:
    prime_assist_psy_forcee = st.number_input(
        "Prime Assistance Psy Totale Forcée (FCFA)",
        min_value=0.0,
        value=float(services_originaux / 2),
        step=1000.0,
        key="prime_assist_psy_forcee_corp",
        help="Prime d'assistance psychologique totale pour tous les assurés"
    )
```

**Calcul avec les nouvelles valeurs :**
```python
services_totaux_forces = prime_lsp_forcee + prime_assist_psy_forcee
prime_ttc_totale_forcee = prime_ttc_taxable_avec_taxe + services_totaux_forces
```

**Sauvegarde mise à jour :**
```python
resultat_micro['services'] = services_totaux_forces
resultat_micro['prime_ttc_totale'] = prime_ttc_totale_forcee
```

#### C. Mise à jour du wrapper `calculer_prime_particuliers`

**Ajout des nouveaux paramètres dans le wrapper :**
```python
def calculer_prime_particuliers(
    # ... paramètres existants ...
    prime_lsp_manuelle: Optional[float] = None,
    prime_assist_psy_manuelle: Optional[float] = None
) -> Dict[str, Any]:
    return calc_calculer_prime_particuliers(
        # ... tous les paramètres ...
        prime_lsp_manuelle=prime_lsp_manuelle,
        prime_assist_psy_manuelle=prime_assist_psy_manuelle,
    )
```

---

## 📊 Impact des Modifications

### ✅ Avantages

1. **Flexibilité accrue** : L'utilisateur peut maintenant ajuster manuellement tous les composants de la prime
2. **Contrôle total** : Pour les barèmes spéciaux et le forçage, tous les montants sont personnalisables
3. **Transparence** : Les valeurs originales sont affichées pour comparaison
4. **Cohérence** : Les mêmes principes s'appliquent pour Particuliers et Corporate

### 📍 Zones Modifiées

- **Barème Spécial Particuliers** : 4 champs au lieu de 2 (Prime Nette + Accessoires + LSP + Assistance Psy)
- **Forçage Corporate Excel** : 4 champs au lieu de 2
- **Calculs** : Prise en compte des nouvelles valeurs manuelles

---

## 🧪 Tests à Effectuer

### Test 1 : Barème Spécial Particuliers
1. Sélectionner "BARÈME SPÉCIAL" dans Cotation Particuliers
2. Remplir les informations du client
3. Vérifier que les 4 champs apparaissent :
   - Prime Nette
   - Accessoires
   - Prime LSP
   - Prime Assistance Psychologique
4. Modifier les valeurs
5. Calculer et vérifier que le résultat reflète les valeurs saisies

### Test 2 : Forçage Corporate Excel
1. Aller dans "Cotation Corporate Excel"
2. Uploader un fichier Excel
3. Calculer la prime
4. Activer le "Forçage Manuel de la Prime"
5. Vérifier que les 4 champs apparaissent :
   - Prime Nette Totale Forcée
   - Accessoires Totaux Forcés
   - Prime LSP Totale Forcée
   - Prime Assistance Psy Totale Forcée
6. Modifier les valeurs
7. Appliquer et vérifier le recalcul

---

## 🔄 Rétrocompatibilité

Les modifications sont **100% rétrocompatibles** :

- Les valeurs par défaut sont conservées (LSP = 20 000 FCFA, Assistance Psy = 35 000 FCFA)
- Les barèmes standards continuent de fonctionner normalement
- Les anciens calculs produisent les mêmes résultats
- Seuls les cas de saisie manuelle sont enrichis

---

## 📦 Fichiers Modifiés

1. ✅ `calculations.py` - Fonction de calcul mise à jour
2. ✅ `santecotation.py` - Interface utilisateur enrichie

---

## 🚀 Déploiement

### Étapes de déploiement :

1. **Sauvegarder les anciens fichiers** (backup)
   ```bash
   cp santecotation.py santecotation.py.backup
   cp calculations.py calculations.py.backup
   ```

2. **Remplacer par les nouveaux fichiers**
   ```bash
   cp santecotation.py /chemin/vers/projet/
   cp calculations.py /chemin/vers/projet/
   ```

3. **Tester localement**
   ```bash
   streamlit run santecotation.py
   ```

4. **Déployer sur Streamlit Cloud**
   - Commiter les changements sur GitHub
   - Les changements seront automatiquement déployés

---

## 📞 Support

En cas de problème ou de question, vérifiez :

1. Que les valeurs par défaut s'affichent correctement
2. Que la modification des champs met à jour le calcul
3. Que les valeurs originales sont bien affichées dans le forçage
4. Que le calcul final prend en compte toutes les composantes

---

**Date de modification :** 09 décembre 2024  
**Version :** 2.0  
**Statut :** ✅ Prêt pour déploiement
