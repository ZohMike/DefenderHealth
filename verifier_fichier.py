#!/usr/bin/env python3
"""
SCRIPT DE VÉRIFICATION - Est-ce que le regroupement est présent ?
Exécutez ce script pour vérifier si votre fichier santecotation.py contient le code de regroupement
"""

import sys
import os

print("="*70)
print("VÉRIFICATION DU FICHIER santecotation.py")
print("="*70)

# Chercher le fichier
if not os.path.exists('santecotation.py'):
    print("\n❌ ERREUR : santecotation.py n'existe pas dans ce répertoire")
    print(f"   Répertoire actuel : {os.getcwd()}")
    sys.exit(1)

# Lire le fichier
with open('santecotation.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Vérifications
checks = {
    "Regroupement intelligent": "# === REGROUPEMENT INTELLIGENT ===",
    "Fonction format_avec_detail": "def format_avec_detail(values):",
    "Groupes defaultdict": "groupes = defaultdict(list)",
    "Clé de regroupement": "key = (produit_name, type_couv)",
    "Population": "population = len(items)",
    "Trop perçu": "trop_percu = st.session_state.get('trop_percu_part_multi'",
    "Montant total": "montant_total = sum(primes_ttc) + trop_percu"
}

print("\n📋 RÉSULTATS :\n")

all_present = True
for name, pattern in checks.items():
    if pattern in content:
        print(f"✅ {name:30s} : PRÉSENT")
    else:
        print(f"❌ {name:30s} : ABSENT !!!")
        all_present = False

print("\n" + "="*70)

if all_present:
    print("✅ SUCCÈS ! Toutes les fonctionnalités sont présentes")
    print("\n📊 Taille du fichier :")
    size = os.path.getsize('santecotation.py')
    print(f"   {size:,} bytes ({size/1024:.1f} KB)")
    
    if size < 180000:
        print("\n⚠️  ATTENTION : Le fichier semble trop petit")
        print("   Attendu : ~186 KB")
        print(f"   Actuel : {size/1024:.1f} KB")
else:
    print("❌ ÉCHEC ! Le fichier est l'ancienne version")
    print("\n🔧 SOLUTION :")
    print("   1. Téléchargez le nouveau santecotation.py")
    print("   2. SUPPRIMEZ l'ancien fichier")
    print("   3. Remplacez-le par le nouveau")
    print("   4. Relancez Streamlit")

print("="*70)
