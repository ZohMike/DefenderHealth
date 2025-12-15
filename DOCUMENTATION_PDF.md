# 📄 Documentation - Générateur PDF de Cotation

## 🎯 Vue d'ensemble

Le module `pdf_generator.py` permet de générer des documents PDF professionnels pour les cotations d'assurance santé, aussi bien pour les **Particuliers** que pour les **Entreprises (Corporate)**.

---

## 📦 Fichiers Fournis

### 1. **pdf_generator.py**
Module principal contenant toute la logique de génération PDF

### 2. **integration_pdf_exemple.py**
Exemples d'intégration dans votre application Streamlit

---

## 🚀 Installation

### Étape 1 : Placer les fichiers

```
votre-projet/
├── santecotation.py
├── calculations.py
├── data.py
├── ui_components.py
├── styles.css
├── pdf_generator.py          ← NOUVEAU
└── requirements.txt
```

### Étape 2 : Vérifier les dépendances

Les dépendances sont déjà dans `requirements.txt` :
```
reportlab>=4.0.0
Pillow>=10.0.0
```

Si vous les ajoutez manuellement :
```bash
pip install reportlab Pillow
```

---

## 💡 Utilisation Rapide

### Pour les Particuliers

```python
from pdf_generator import generer_pdf_cotation_particulier
import uuid
from datetime import datetime

# 1. Générer un numéro de devis
numero_devis = f"PART-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

# 2. Préparer les informations
client_info = {
    'nom': 'KOUAME',
    'prenom': 'Jean',
    'contact': '+225 07 12 34 56 78',
    'type_couverture': 'Famille',
    'nb_enfants': 2
}

# 3. Générer le PDF
pdf_bytes = generer_pdf_cotation_particulier(
    resultat=resultat,  # Votre résultat de calcul
    produit_name="80% CI RUBIS",
    client_info=client_info,
    numero_devis=numero_devis
)

# 4. Dans Streamlit - Bouton de téléchargement
st.download_button(
    label="📥 Télécharger le PDF",
    data=pdf_bytes,
    file_name=f"Cotation_{numero_devis}.pdf",
    mime="application/pdf",
    type="primary"
)
```

### Pour les Entreprises (Corporate)

```python
from pdf_generator import generer_pdf_cotation_corporate

# 1. Numéro de devis
numero_devis = f"CORP-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

# 2. Informations entreprise
entreprise_info = {
    'nom': 'SARL IVOIRE TECH',
    'secteur': 'Technologies de l\'information'
}

# 3. Générer le PDF
pdf_bytes = generer_pdf_cotation_corporate(
    resultat=resultat,
    produit_name="80% CI",
    entreprise_info=entreprise_info,
    numero_devis=numero_devis
)

# 4. Téléchargement
st.download_button(
    label="📥 Télécharger PDF Corporate",
    data=pdf_bytes,
    file_name=f"Proposition_{numero_devis}.pdf",
    mime="application/pdf"
)
```

---

## 📊 Structure des Données

### Resultat (Dict)

```python
resultat = {
    # OBLIGATOIRES
    'prime_nette_finale': float,      # Prime nette calculée
    'accessoires': float,              # Frais accessoires
    'taxe': float,                     # Montant de la taxe
    'prime_ttc_totale': float,         # Prime TTC totale
    
    # SERVICES
    'prime_lsp': float,                # Prime LSP
    'prime_assist_psy': float,         # Prime assistance psy
    
    # OPTIONNELS - Surprimes
    'surprime_grossesse': float,       # Montant surprime grossesse
    'surprime_age_taux': float,        # Taux surprime âge (%)
    'surprime_risques_taux': float,    # Taux surprime médicale (%)
    
    # OPTIONNELS - Affections
    'affections_declarees': list,      # Liste des affections
    
    # FLAGS
    'bareme_special': bool,            # Si barème spécial
    
    # FACTEURS
    'facteurs': {
        'duree_contrat': int,          # Durée en mois
        'taux_taxe': float             # Taux de taxe (0.08 ou 0.03)
    },
    
    # CORPORATE SEULEMENT
    'nb_familles': int,
    'nb_personnes_seules': int,
    'nb_enfants_supplementaires': int,
    'type_calcul': str                 # 'estimation_rapide' ou autre
}
```

### Client Info (Dict) - Particuliers

```python
client_info = {
    'nom': str,                        # Nom du client
    'prenom': str,                     # Prénom du client
    'contact': str,                    # Numéro de téléphone
    'type_couverture': str,            # 'Personne seule' ou 'Famille'
    'nb_enfants': int                  # Nombre d'enfants (si famille)
}
```

### Entreprise Info (Dict) - Corporate

```python
entreprise_info = {
    'nom': str,                        # Raison sociale
    'secteur': str                     # Secteur d'activité
}
```

---

## 🎨 Personnalisation

### Modifier les Couleurs

Dans `pdf_generator.py`, classe `PDFGenerator`, méthode `_setup_custom_styles()` :

```python
# Couleur principale (titres)
textColor=colors.HexColor('#1a1d29')  # Noir foncé

# Couleur accent (sous-titres)
textColor=colors.HexColor('#2196F3')  # Bleu

# Couleur sections (Corporate)
textColor=colors.HexColor('#145d33')  # Vert
```

### Ajouter un Logo

Dans la méthode `_add_header()` :

```python
def _add_header(self, canvas_obj, doc):
    canvas_obj.saveState()
    
    # Ajouter votre logo
    logo_path = "path/to/your/logo.png"
    canvas_obj.drawImage(logo_path, 40, A4[1] - 70, width=100, height=50)
    
    # ... reste du code
```

### Modifier les Mentions Légales

Dans les méthodes `generer_pdf_particulier()` et `generer_pdf_corporate()` :

```python
mentions = (
    "Votre texte personnalisé ici..."
)
```

---

## 📋 Intégration dans Streamlit

### Option 1 : Après le Calcul de Prime

```python
# Après avoir affiché le résultat avec afficher_resultat()

st.markdown("---")
st.markdown("### 📄 Document de Cotation")

# Générer numéro de devis
if 'numero_devis' not in st.session_state:
    st.session_state['numero_devis'] = f"PART-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"

# Préparer les infos
client_info = {
    'nom': principal_data['nom'],
    'prenom': principal_data['prenom'],
    'contact': principal_data['contact'],
    'type_couverture': type_couverture_part,
    'nb_enfants': nb_enfants_part
}

# Générer PDF
try:
    pdf_bytes = generer_pdf_cotation_particulier(
        resultat=resultat,
        produit_name=PRODUITS_PARTICULIERS_UI[produit_key_part],
        client_info=client_info,
        numero_devis=st.session_state['numero_devis']
    )
    
    # Bouton téléchargement
    st.download_button(
        label="📥 Télécharger le PDF",
        data=pdf_bytes,
        file_name=f"Cotation_{st.session_state['numero_devis']}.pdf",
        mime="application/pdf",
        type="primary",
        use_container_width=True
    )
    
except Exception as e:
    st.error(f"❌ Erreur : {str(e)}")
```

### Option 2 : Dans une Section Dédiée

```python
# Créer un expander pour le PDF
with st.expander("📄 Générer le Document PDF", expanded=False):
    st.info("💡 Téléchargez un document PDF professionnel")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"**Client :** {client_info['nom']} {client_info['prenom']}")
        st.markdown(f"**Produit :** {produit_name}")
        st.markdown(f"**Prime :** {format_currency(resultat['prime_ttc_totale'])}")
    
    with col2:
        pdf_bytes = generer_pdf_cotation_particulier(...)
        st.download_button(...)
```

### Option 3 : Pour Plusieurs Barèmes

```python
# Si vous comparez plusieurs barèmes
st.markdown("### 📄 Documents PDF")

for idx, bareme_key in enumerate(baremes_affiches):
    resultat = resultats_multi[idx]['resultat']
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.markdown(f"**{PRODUITS_PARTICULIERS_UI[bareme_key]}**")
        st.caption(f"Prime TTC: {format_currency(resultat['prime_ttc_totale'])}")
    
    with col2:
        numero = f"PART-{datetime.now().strftime('%Y%m%d')}-{idx+1:02d}"
        pdf_bytes = generer_pdf_cotation_particulier(
            resultat=resultat,
            produit_name=PRODUITS_PARTICULIERS_UI[bareme_key],
            client_info=client_info,
            numero_devis=numero
        )
        
        st.download_button(
            label="📥 PDF",
            data=pdf_bytes,
            file_name=f"Cotation_{numero}.pdf",
            mime="application/pdf",
            key=f"pdf_{idx}"
        )
```

---

## 🎨 Aperçu du Document Généré

### Structure du PDF Particulier

```
┌─────────────────────────────────────┐
│  🛡️ ASSUR DEFENDER                  │
│  Cotation Santé +        09/12/2024│
├─────────────────────────────────────┤
│                                     │
│  PROPOSITION DE COTATION SANTÉ      │
│                                     │
│  Devis N° : PART-20241209-A3F2B1   │
│                                     │
│  ───── INFORMATIONS CLIENT ─────    │
│  │ Nom et Prénom │ KOUAME Jean   │  │
│  │ Contact       │ +225 07...    │  │
│  │ Type          │ Famille       │  │
│  │ Produit       │ 80% CI RUBIS  │  │
│  └───────────────┴───────────────┘  │
│                                     │
│  ───── DÉTAIL DE LA PRIME ─────     │
│  │ Désignation            │Montant│ │
│  │ Prime Nette           │324 266│ │
│  │ Accessoires           │ 10 000│ │
│  │ Sous-total HT         │334 266│ │
│  │ Taxe (8%)             │ 26 741│ │
│  │ Prime LSP             │ 20 000│ │
│  │ Prime Assist Psy      │ 35 000│ │
│  │ PRIME TOTALE TTC      │416 007│ │
│  └───────────────────────┴───────┘  │
│                                     │
│       MONTANT TOTAL À PAYER         │
│          416 007 FCFA               │
│                                     │
│  Durée du contrat : 12 mois         │
│                                     │
│  ───── CONDITIONS ─────              │
│  ✓ Valable 30 jours                │
│  ✓ Questionnaire médical requis    │
│  ✓ Effet dès paiement              │
│  ...                               │
│                                     │
├─────────────────────────────────────┤
│  Page 1    www.assurdefender.ci    │
└─────────────────────────────────────┘
```

### Structure du PDF Corporate

```
┌─────────────────────────────────────┐
│  🛡️ ASSUR DEFENDER                  │
│  Cotation Santé +        09/12/2024│
├─────────────────────────────────────┤
│                                     │
│  PROPOSITION COMMERCIALE            │
│  Assurance Santé Collective         │
│                                     │
│  Devis N° : CORP-20241209-X7Y9Z2   │
│                                     │
│  ───── INFORMATIONS ENTREPRISE ──── │
│  │ Raison sociale│ SARL IVOIRE... │ │
│  │ Secteur       │ Technologies  │  │
│  │ Produit       │ 80% CI        │  │
│  │ Familles      │ 10            │  │
│  │ Personnes     │ 5             │  │
│  │ Total unités  │ 15            │  │
│  └───────────────┴───────────────┘  │
│                                     │
│  ───── DÉTAIL COTISATION ─────      │
│  │ Prime Nette Totale  │6 987 300│ │
│  │ Accessoires         │  150 000│ │
│  │ Sous-total HT       │7 137 300│ │
│  │ Taxe (3%)           │  214 119│ │
│  │ Prime LSP           │  300 000│ │
│  │ Assist Psy          │  525 000│ │
│  │ COTISATION TTC      │8 176 419│ │
│  └─────────────────────┴─────────┘  │
│                                     │
│      COTISATION ANNUELLE            │
│         8 176 419 FCFA              │
│                                     │
│  Soit ~545 095 FCFA par unité       │
│                                     │
│  ───── GARANTIES ─────               │
│  ✓ Consultations et soins          │
│  ✓ Hospitalisation                 │
│  ...                               │
│                                     │
│  ───── PROCHAINES ÉTAPES ─────      │
│  1. Validation proposition         │
│  2. Questionnaires médicaux        │
│  ...                               │
│                                     │
└─────────────────────────────────────┘
```

---

## 🔧 Dépannage

### Erreur : Module 'reportlab' not found

```bash
pip install reportlab Pillow
```

### Erreur : Cannot import 'generer_pdf_cotation_particulier'

Vérifiez que `pdf_generator.py` est dans le même dossier que `santecotation.py`

### PDF ne se génère pas

Vérifiez la structure de votre `resultat` :
```python
print(resultat.keys())  # Doit contenir au minimum les clés obligatoires
```

### Texte mal affiché dans le PDF

Vérifiez les caractères spéciaux. ReportLab supporte l'UTF-8.

---

## 📊 Fonctionnalités Avancées

### Ajouter un QR Code

```python
from reportlab.graphics.barcode import qr

# Dans _add_header()
qr_code = qr.QrCodeWidget(f"https://assurdefender.ci/devis/{numero_devis}")
qr_bounds = qr_code.getBounds()
qr_width = qr_bounds[2] - qr_bounds[0]
qr_height = qr_bounds[3] - qr_bounds[1]

# Dessiner le QR code
canvas_obj.drawPath(qr_code)
```

### Ajouter des Graphiques

```python
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie

# Créer un graphique
drawing = Drawing(400, 200)
pie = Pie()
pie.x = 150
pie.y = 50
pie.data = [60, 30, 10]
pie.labels = ['Prime', 'Services', 'Taxe']
drawing.add(pie)

story.append(drawing)
```

---

## ✅ Checklist de Déploiement

- [ ] `pdf_generator.py` placé dans le projet
- [ ] `requirements.txt` mis à jour
- [ ] Import ajouté dans `santecotation.py`
- [ ] Code d'intégration ajouté après les calculs
- [ ] Test local effectué
- [ ] Logo personnalisé ajouté (optionnel)
- [ ] Couleurs personnalisées (optionnel)
- [ ] Mentions légales vérifiées
- [ ] Déployé sur Streamlit Cloud

---

## 📞 Support

Pour toute question sur l'implémentation, référez-vous à :
- **integration_pdf_exemple.py** - Exemples détaillés
- Documentation ReportLab : https://www.reportlab.com/docs/

---

**Bonne génération de PDF ! 📄✨**
