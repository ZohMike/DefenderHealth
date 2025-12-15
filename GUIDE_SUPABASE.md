# 🚀 Guide de Configuration Supabase pour Assur Defender

Ce guide vous accompagne étape par étape pour connecter votre application à Supabase.

---

## 📋 Table des matières

1. [Prérequis](#prérequis)
2. [Création du projet Supabase](#création-du-projet-supabase)
3. [Configuration de la base de données](#configuration-de-la-base-de-données)
4. [Configuration locale](#configuration-locale)
5. [Déploiement sur Streamlit Cloud](#déploiement-sur-streamlit-cloud)
6. [Intégration dans votre application](#intégration-dans-votre-application)
7. [Tests](#tests)

---

## 1️⃣ Prérequis

- Un compte Supabase (gratuit) : https://supabase.com
- Votre projet déjà sur GitHub
- Python 3.8+ installé localement

---

## 2️⃣ Création du projet Supabase

### Étape 1 : Créer un compte et un projet

1. Allez sur https://supabase.com
2. Cliquez sur **"Start your project"**
3. Connectez-vous avec GitHub (recommandé)
4. Cliquez sur **"New Project"**
5. Remplissez les informations :
   - **Name** : `assur-defender` (ou votre choix)
   - **Database Password** : Choisissez un mot de passe fort (NOTEZ-LE !)
   - **Region** : Choisissez la plus proche (ex: Europe West)
6. Cliquez sur **"Create new project"**
7. Attendez 2-3 minutes que le projet soit provisionné

---

## 3️⃣ Configuration de la base de données

### Étape 2 : Créer les tables

1. Dans votre projet Supabase, allez dans **SQL Editor** (icône dans le menu gauche)
2. Cliquez sur **"New query"**
3. Copiez TOUT le contenu du fichier `supabase_schema.sql`
4. Collez-le dans l'éditeur
5. Cliquez sur **"Run"** (bouton en bas à droite)
6. Vérifiez qu'il n'y a pas d'erreurs (vous devriez voir "Success")

### Étape 3 : Vérifier les tables créées

1. Allez dans **Table Editor** (menu gauche)
2. Vous devriez voir 5 tables :
   - ✅ `devis`
   - ✅ `assures`
   - ✅ `cotations_excel`
   - ✅ `historique_modifications`
   - ✅ `utilisateurs`

---

## 4️⃣ Configuration locale

### Étape 4 : Obtenir vos credentials

1. Dans votre projet Supabase, allez dans **Settings** > **API**
2. Notez ces deux informations :
   - **Project URL** : `https://xxxxx.supabase.co`
   - **anon/public key** : `eyJhbGciOi...` (longue clé)

### Étape 5 : Créer le fichier de secrets local

1. Dans votre projet, créez un dossier `.streamlit` (s'il n'existe pas déjà)
   ```bash
   mkdir .streamlit
   ```

2. Créez le fichier `.streamlit/secrets.toml`
   ```bash
   # Sur Windows
   type nul > .streamlit\secrets.toml
   
   # Sur Mac/Linux
   touch .streamlit/secrets.toml
   ```

3. Ouvrez `.streamlit/secrets.toml` et ajoutez :
   ```toml
   [supabase]
   url = "https://xxxxx.supabase.co"  # Remplacez par votre URL
   key = "eyJhbGci..."  # Remplacez par votre clé anon
   ```

4. **IMPORTANT** : Vérifiez que `.streamlit/` est dans votre `.gitignore` !

### Étape 6 : Installer les dépendances

```bash
pip install -r requirements.txt
```

### Étape 7 : Ajouter les fichiers à votre projet

Ajoutez ces fichiers à votre projet :
- ✅ `supabase_config.py`
- ✅ `database.py`
- ✅ `.gitignore` (mise à jour)
- ✅ `requirements.txt` (mise à jour)

---

## 5️⃣ Déploiement sur Streamlit Cloud

### Étape 8 : Configurer les secrets sur Streamlit Cloud

1. Allez sur https://share.streamlit.io
2. Sélectionnez votre application
3. Cliquez sur **⚙️ Settings** (en haut à droite)
4. Cliquez sur **Secrets**
5. Collez le contenu de votre fichier `.streamlit/secrets.toml` :
   ```toml
   [supabase]
   url = "https://xxxxx.supabase.co"
   key = "eyJhbGci..."
   ```
6. Cliquez sur **Save**

### Étape 9 : Redéployer l'application

L'application se redéploiera automatiquement avec les nouvelles dépendances.

---

## 6️⃣ Intégration dans votre application

### Étape 10 : Modifier santecotation.py

Ajoutez ces imports au début du fichier :

```python
from database import DatabaseManager
import uuid
```

### Étape 11 : Initialiser le gestionnaire de base de données

Après la configuration de la page, ajoutez :

```python
# Initialisation de la base de données
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = DatabaseManager()
```

### Étape 12 : Sauvegarder les devis

Exemple pour sauvegarder un devis Particulier après calcul :

```python
# Après le calcul de la prime (dans la section Particuliers)
if st.button("💾 SAUVEGARDER LE DEVIS"):
    # Générer un numéro de devis unique
    numero_devis = f"PART-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
    
    # Préparer les données du devis
    devis_data = {
        'numero_devis': numero_devis,
        'type_marche': 'Particulier',
        'produit': PRODUITS_PARTICULIERS_UI[produit_key_part],
        'nom_client': f"{principal_data['nom']} {principal_data['prenom']}",
        'type_couverture': type_couverture_part,
        'nb_adultes': 2 if type_couverture_part == "Famille" else 1,
        'nb_enfants': nb_enfants_part,
        'nb_enfants_supplementaires': enfants_supplementaires_part,
        'prime_nette': resultat['prime_nette_finale'],
        'accessoires': resultat['accessoires'],
        'services': resultat['services'],
        'taxe': resultat['taxe'],
        'prime_ttc': resultat['prime_ttc_taxable'],
        'prime_finale': resultat['prime_finale'],
        'reduction_commerciale': reduction_commerciale_part,
        'surprime_medicale': resultat.get('taux_surprime_medicale', 0),
        'surprime_age': resultat.get('taux_surprime_age', 0),
        'duree_contrat': duree_contrat_part,
        'statut': 'Finalisé',
        'created_by': 'Utilisateur',  # À remplacer par le vrai utilisateur si vous avez un système d'auth
        'details': {
            'principal': principal_data,
            'conjoint': conjoint_data if type_couverture_part == "Famille" else None,
            'enfants': enfants_data if nb_enfants_part > 0 else []
        }
    }
    
    # Sauvegarder dans Supabase
    devis_sauvegarde = st.session_state.db_manager.sauvegarder_devis(devis_data)
    
    if devis_sauvegarde:
        st.success(f"✅ Devis **{numero_devis}** sauvegardé avec succès !")
        
        # Sauvegarder les assurés
        # Principal
        assure_principal = {
            'numero_devis': numero_devis,
            'type_assure': 'Principal',
            **principal_data,
            'imc': calculer_imc(principal_data['poids'], principal_data['taille'])[0]
        }
        st.session_state.db_manager.sauvegarder_assure(assure_principal)
        
        # Conjoint (si famille)
        if type_couverture_part == "Famille" and conjoint_data:
            assure_conjoint = {
                'numero_devis': numero_devis,
                'type_assure': 'Conjoint',
                **conjoint_data,
                'imc': calculer_imc(conjoint_data['poids'], conjoint_data['taille'])[0]
            }
            st.session_state.db_manager.sauvegarder_assure(assure_conjoint)
        
        # Enfants
        if nb_enfants_part > 0 and enfants_data:
            for enfant in enfants_data:
                assure_enfant = {
                    'numero_devis': numero_devis,
                    'type_assure': 'Enfant',
                    **enfant,
                    'imc': calculer_imc(enfant['poids'], enfant['taille'])[0]
                }
                st.session_state.db_manager.sauvegarder_assure(assure_enfant)
```

### Étape 13 : Afficher les devis sauvegardés

Dans l'onglet "Gestion des Devis", ajoutez :

```python
# Récupérer les devis
devis_list = st.session_state.db_manager.recuperer_devis(limit=50)

if devis_list:
    st.success(f"✅ {len(devis_list)} devis trouvés")
    
    # Afficher sous forme de tableau
    df_devis = pd.DataFrame(devis_list)
    st.dataframe(df_devis[[
        'numero_devis', 'type_marche', 'produit', 
        'nom_client', 'prime_finale', 'statut', 'date_creation'
    ]])
else:
    st.info("Aucun devis trouvé")
```

---

## 7️⃣ Tests

### Étape 14 : Tester la connexion

Ajoutez ce code temporaire pour tester :

```python
if st.button("🔍 Tester la connexion Supabase"):
    from supabase_config import test_connexion_supabase
    if test_connexion_supabase():
        st.success("✅ Connexion réussie à Supabase !")
    else:
        st.error("❌ Échec de la connexion")
```

### Étape 15 : Créer un devis de test

1. Lancez votre application localement : `streamlit run santecotation.py`
2. Allez dans "Cotation Particuliers"
3. Remplissez un formulaire de test
4. Calculez la prime
5. Cliquez sur "Sauvegarder le devis"
6. Vérifiez dans Supabase (Table Editor > devis) que le devis apparaît

---

## 🎉 Félicitations !

Votre application est maintenant connectée à Supabase ! Vous pouvez :

✅ Sauvegarder les devis automatiquement  
✅ Consulter l'historique des cotations  
✅ Générer des statistiques  
✅ Rechercher des devis  
✅ Exporter les données  

---

## 📊 Fonctionnalités supplémentaires

### Afficher des statistiques

```python
stats = st.session_state.db_manager.get_statistiques_globales()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Devis", stats.get('total_devis', 0))
col2.metric("Finalisés", stats.get('devis_finalises', 0))
col3.metric("En attente", stats.get('devis_en_attente', 0))
col4.metric("Total Primes", format_currency(stats.get('total_primes', 0)))
```

### Rechercher des devis

```python
nom_recherche = st.text_input("🔍 Rechercher par nom")
if nom_recherche:
    resultats = st.session_state.db_manager.rechercher_devis(nom_client=nom_recherche)
    st.dataframe(resultats)
```

---

## 🆘 Besoin d'aide ?

**Erreur de connexion ?**
- Vérifiez vos credentials dans `.streamlit/secrets.toml`
- Vérifiez que le projet Supabase est bien actif
- Vérifiez les policies RLS dans Supabase

**Erreur SQL ?**
- Vérifiez que toutes les tables sont créées
- Relancez le script `supabase_schema.sql`

**Données non sauvegardées ?**
- Vérifiez les logs de l'application
- Vérifiez les policies RLS (Row Level Security)

---

## 📚 Ressources

- Documentation Supabase : https://supabase.com/docs
- Documentation Streamlit : https://docs.streamlit.io
- Supabase Python Client : https://github.com/supabase-community/supabase-py

---

**Bonne utilisation ! 🚀**
