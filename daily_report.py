#!/usr/bin/env python3
"""
Script de rapport journalier - SANTÉ+ Cotation
Envoie un email quotidien à 18h avec les statistiques du jour.

Configuration:
- Peut être exécuté via cron: 0 18 * * * /usr/bin/python3 /path/to/daily_report.py
- Ou via GitHub Actions / Supabase Edge Functions

Email envoyé à: m-zoh@leadway.com
"""

import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from supabase import create_client, Client
import json

# ==================== CONFIGURATION ====================

# Destinataire du rapport
DESTINATAIRE = "m-zoh@leadway.com"

# Configuration SMTP (à configurer selon votre serveur mail)
# Pour Gmail: smtp.gmail.com, port 587
# Pour Outlook: smtp.office365.com, port 587
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")  # Email expéditeur
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")  # Mot de passe ou App Password

# Configuration Supabase
SUPABASE_URL = os.environ.get("SUPABASE_URL", "")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "")


def get_supabase_client() -> Client:
    """Crée et retourne le client Supabase."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("Variables SUPABASE_URL et SUPABASE_KEY requises")
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def get_daily_stats() -> dict:
    """
    Récupère les statistiques du jour.
    
    Returns:
        Dict avec les statistiques du jour
    """
    client = get_supabase_client()
    
    # Date du jour (début et fin)
    today = datetime.now().date()
    today_start = datetime.combine(today, datetime.min.time()).isoformat()
    today_end = datetime.combine(today, datetime.max.time()).isoformat()
    
    stats = {
        'date': today.strftime("%d/%m/%Y"),
        'cotations_jour': 0,
        'cotations_particulier': 0,
        'cotations_corporate': 0,
        'polices_creees': 0,
        'volume_primes_jour': 0,
        'cotations_finalisees': 0,
        'cotations_en_attente': 0,
        'total_cotations': 0,
        'total_polices': 0
    }
    
    try:
        # Cotations du jour
        cotations_jour = client.table('devis').select('*').gte(
            'date_creation', today_start
        ).lte('date_creation', today_end).execute()
        
        stats['cotations_jour'] = len(cotations_jour.data) if cotations_jour.data else 0
        
        if cotations_jour.data:
            stats['cotations_particulier'] = len([c for c in cotations_jour.data if c.get('type_marche') == 'Particulier'])
            stats['cotations_corporate'] = len([c for c in cotations_jour.data if c.get('type_marche') == 'Corporate'])
            stats['volume_primes_jour'] = sum([c.get('prime_finale', 0) or 0 for c in cotations_jour.data])
        
        # Polices créées aujourd'hui
        polices_jour = client.table('polices').select('*').gte(
            'date_creation', today_start
        ).lte('date_creation', today_end).execute()
        
        stats['polices_creees'] = len(polices_jour.data) if polices_jour.data else 0
        
        # Totaux globaux
        all_cotations = client.table('devis').select('id, statut').execute()
        if all_cotations.data:
            stats['total_cotations'] = len(all_cotations.data)
            stats['cotations_finalisees'] = len([c for c in all_cotations.data if c.get('statut') == 'Finalisé'])
            stats['cotations_en_attente'] = len([c for c in all_cotations.data if c.get('statut') in ['En attente', 'En cours']])
        
        all_polices = client.table('polices').select('id').execute()
        stats['total_polices'] = len(all_polices.data) if all_polices.data else 0
        
    except Exception as e:
        print(f"Erreur lors de la récupération des stats: {e}")
    
    return stats


def format_number(n: float) -> str:
    """Formate un nombre avec séparateur de milliers."""
    return f"{int(n):,}".replace(',', ' ')


def create_email_html(stats: dict) -> str:
    """
    Crée le contenu HTML de l'email.
    
    Args:
        stats: Dictionnaire des statistiques
        
    Returns:
        HTML formaté
    """
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: #f5f5f5;
                margin: 0;
                padding: 20px;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                background-color: white;
                border-radius: 10px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                overflow: hidden;
            }}
            .header {{
                background: linear-gradient(135deg, #6A0DAD 0%, #4A0882 100%);
                color: white;
                padding: 30px;
                text-align: center;
            }}
            .header h1 {{
                margin: 0;
                font-size: 24px;
            }}
            .header .date {{
                opacity: 0.9;
                margin-top: 10px;
                font-size: 14px;
            }}
            .content {{
                padding: 30px;
            }}
            .section-title {{
                color: #6A0DAD;
                font-size: 18px;
                font-weight: bold;
                margin-bottom: 15px;
                border-bottom: 2px solid #6A0DAD;
                padding-bottom: 5px;
            }}
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(2, 1fr);
                gap: 15px;
                margin-bottom: 25px;
            }}
            .stat-card {{
                background: #f8f5fc;
                border-radius: 8px;
                padding: 15px;
                text-align: center;
            }}
            .stat-card .number {{
                font-size: 28px;
                font-weight: bold;
                color: #6A0DAD;
            }}
            .stat-card .label {{
                font-size: 12px;
                color: #666;
                margin-top: 5px;
            }}
            .highlight {{
                background: linear-gradient(135deg, #6A0DAD 0%, #4A0882 100%);
                color: white !important;
            }}
            .highlight .number, .highlight .label {{
                color: white !important;
            }}
            .summary {{
                background: #e8f5e9;
                border-left: 4px solid #4CAF50;
                padding: 15px;
                margin: 20px 0;
                border-radius: 0 8px 8px 0;
            }}
            .footer {{
                background: #f5f5f5;
                padding: 20px;
                text-align: center;
                font-size: 12px;
                color: #666;
            }}
            .footer a {{
                color: #6A0DAD;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Rapport Quotidien SANTÉ+</h1>
                <div class="date">Leadway Assurance - {stats['date']}</div>
            </div>
            
            <div class="content">
                <div class="section-title">📈 Activité du jour</div>
                <div class="stats-grid">
                    <div class="stat-card highlight">
                        <div class="number">{stats['cotations_jour']}</div>
                        <div class="label">Cotations créées</div>
                    </div>
                    <div class="stat-card highlight">
                        <div class="number">{stats['polices_creees']}</div>
                        <div class="label">Polices émises</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['cotations_particulier']}</div>
                        <div class="label">Particuliers</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['cotations_corporate']}</div>
                        <div class="label">Corporate</div>
                    </div>
                </div>
                
                <div class="summary">
                    <strong>💰 Volume des primes du jour:</strong> {format_number(stats['volume_primes_jour'])} FCFA
                </div>
                
                <div class="section-title">📋 État général du portefeuille</div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="number">{stats['total_cotations']}</div>
                        <div class="label">Total cotations</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['total_polices']}</div>
                        <div class="label">Total polices</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['cotations_finalisees']}</div>
                        <div class="label">Cotations finalisées</div>
                    </div>
                    <div class="stat-card">
                        <div class="number">{stats['cotations_en_attente']}</div>
                        <div class="label">En attente</div>
                    </div>
                </div>
            </div>
            
            <div class="footer">
                <p>Ce rapport est généré automatiquement par l'application SANTÉ+ Cotation.</p>
                <p><a href="#">Accéder à l'application</a></p>
                <p style="margin-top: 10px;">© {datetime.now().year} Leadway Assurance Vie</p>
            </div>
        </div>
    </body>
    </html>
    """
    return html


def create_email_text(stats: dict) -> str:
    """
    Crée le contenu texte de l'email (fallback).
    
    Args:
        stats: Dictionnaire des statistiques
        
    Returns:
        Texte formaté
    """
    return f"""
RAPPORT QUOTIDIEN SANTÉ+ - {stats['date']}
============================================

📈 ACTIVITÉ DU JOUR
- Cotations créées: {stats['cotations_jour']}
- Polices émises: {stats['polices_creees']}
- Particuliers: {stats['cotations_particulier']}
- Corporate: {stats['cotations_corporate']}
- Volume des primes: {format_number(stats['volume_primes_jour'])} FCFA

📋 ÉTAT GÉNÉRAL
- Total cotations: {stats['total_cotations']}
- Total polices: {stats['total_polices']}
- Cotations finalisées: {stats['cotations_finalisees']}
- En attente: {stats['cotations_en_attente']}

---
Rapport généré automatiquement par SANTÉ+ Cotation
© {datetime.now().year} Leadway Assurance Vie
    """


def send_email(stats: dict) -> bool:
    """
    Envoie l'email avec les statistiques.
    
    Args:
        stats: Dictionnaire des statistiques
        
    Returns:
        True si succès, False sinon
    """
    if not SMTP_USER or not SMTP_PASSWORD:
        print("⚠️ Configuration SMTP manquante. Email non envoyé.")
        print("Variables requises: SMTP_USER, SMTP_PASSWORD")
        return False
    
    try:
        # Créer le message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = f"📊 Rapport SANTÉ+ du {stats['date']} - {stats['cotations_jour']} cotations, {stats['polices_creees']} polices"
        msg['From'] = SMTP_USER
        msg['To'] = DESTINATAIRE
        
        # Ajouter les parties texte et HTML
        text_part = MIMEText(create_email_text(stats), 'plain', 'utf-8')
        html_part = MIMEText(create_email_html(stats), 'html', 'utf-8')
        
        msg.attach(text_part)
        msg.attach(html_part)
        
        # Envoyer l'email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, DESTINATAIRE, msg.as_string())
        
        print(f"✅ Email envoyé avec succès à {DESTINATAIRE}")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi: {e}")
        return False


def main():
    """Fonction principale."""
    print("=" * 50)
    print(f"📊 RAPPORT QUOTIDIEN SANTÉ+ - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 50)
    
    # Récupérer les statistiques
    print("\n📈 Récupération des statistiques...")
    stats = get_daily_stats()
    
    # Afficher les stats
    print(f"\n📅 Date: {stats['date']}")
    print(f"📝 Cotations du jour: {stats['cotations_jour']}")
    print(f"   - Particuliers: {stats['cotations_particulier']}")
    print(f"   - Corporate: {stats['cotations_corporate']}")
    print(f"📋 Polices créées: {stats['polices_creees']}")
    print(f"💰 Volume du jour: {format_number(stats['volume_primes_jour'])} FCFA")
    print(f"\n📊 Totaux:")
    print(f"   - Cotations: {stats['total_cotations']}")
    print(f"   - Polices: {stats['total_polices']}")
    
    # Envoyer l'email
    print(f"\n📧 Envoi de l'email à {DESTINATAIRE}...")
    success = send_email(stats)
    
    if success:
        print("\n✅ Rapport envoyé avec succès!")
    else:
        print("\n⚠️ Email non envoyé - vérifiez la configuration SMTP")
    
    print("=" * 50)


if __name__ == "__main__":
    main()

