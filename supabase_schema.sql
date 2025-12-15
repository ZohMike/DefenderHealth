-- =====================================================
-- SCRIPT DE CRÉATION DES TABLES SUPABASE
-- Application: Assur Defender - Cotation Santé+
-- =====================================================

-- Table: devis
-- Stocke toutes les cotations/devis créés
CREATE TABLE IF NOT EXISTS devis (
    id BIGSERIAL PRIMARY KEY,
    numero_devis VARCHAR(50) UNIQUE NOT NULL,
    type_marche VARCHAR(20) NOT NULL CHECK (type_marche IN ('Particulier', 'Corporate')),
    produit VARCHAR(100) NOT NULL,
    nom_client VARCHAR(200),
    entreprise VARCHAR(200),
    secteur VARCHAR(100),
    type_couverture VARCHAR(50),
    nb_adultes INTEGER DEFAULT 1,
    nb_enfants INTEGER DEFAULT 0,
    nb_enfants_supplementaires INTEGER DEFAULT 0,
    prime_nette DECIMAL(15,2) DEFAULT 0,
    accessoires DECIMAL(15,2) DEFAULT 0,
    services DECIMAL(15,2) DEFAULT 0,
    taxe DECIMAL(15,2) DEFAULT 0,
    prime_ttc DECIMAL(15,2) DEFAULT 0,
    prime_finale DECIMAL(15,2) DEFAULT 0,
    reduction_commerciale DECIMAL(5,2) DEFAULT 0,
    surprime_medicale DECIMAL(5,2) DEFAULT 0,
    surprime_age DECIMAL(5,2) DEFAULT 0,
    duree_contrat INTEGER DEFAULT 12,
    statut VARCHAR(20) DEFAULT 'En attente' CHECK (statut IN ('En attente', 'En cours', 'Finalisé', 'Annulé')),
    validateur VARCHAR(200),
    motif_reduction TEXT,
    details JSONB,
    pdf_data TEXT,  -- PDF stocké en base64 pour téléchargement identique
    created_by VARCHAR(100) DEFAULT 'Système',
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index sur les colonnes fréquemment recherchées
CREATE INDEX idx_devis_numero ON devis(numero_devis);
CREATE INDEX idx_devis_statut ON devis(statut);
CREATE INDEX idx_devis_type_marche ON devis(type_marche);
CREATE INDEX idx_devis_date_creation ON devis(date_creation DESC);
CREATE INDEX idx_devis_entreprise ON devis(entreprise);

-- =====================================================

-- Table: assures
-- Stocke les informations détaillées de chaque assuré
CREATE TABLE IF NOT EXISTS assures (
    id BIGSERIAL PRIMARY KEY,
    numero_devis VARCHAR(50) NOT NULL REFERENCES devis(numero_devis) ON DELETE CASCADE,
    type_assure VARCHAR(20) NOT NULL CHECK (type_assure IN ('Principal', 'Conjoint', 'Enfant')),
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    date_naissance DATE NOT NULL,
    lieu_naissance VARCHAR(100),
    contact VARCHAR(50),
    numero_cnam VARCHAR(50),
    nationalite VARCHAR(50) DEFAULT 'Ivoirienne',
    etat_civil VARCHAR(30),
    emploi_actuel VARCHAR(100),
    taille INTEGER,
    poids INTEGER,
    imc DECIMAL(4,1),
    tension_arterielle VARCHAR(20),
    affections JSONB DEFAULT '[]',
    grossesse BOOLEAN DEFAULT FALSE,
    sexe VARCHAR(10),
    details JSONB,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_assures_devis ON assures(numero_devis);
CREATE INDEX idx_assures_type ON assures(type_assure);
CREATE INDEX idx_assures_nom ON assures(nom, prenom);

-- =====================================================

-- Table: polices
-- Stocke les polices d'assurance créées à partir des cotations
CREATE TABLE IF NOT EXISTS polices (
    id BIGSERIAL PRIMARY KEY,
    numero_police VARCHAR(50) UNIQUE NOT NULL,
    cotation_id BIGINT REFERENCES devis(id) ON DELETE SET NULL,
    assure_principal VARCHAR(200) NOT NULL,
    type_police VARCHAR(20) NOT NULL CHECK (type_police IN ('particulier', 'corporate')),
    produit VARCHAR(100) NOT NULL,
    date_effet DATE NOT NULL,
    date_echeance DATE NOT NULL,
    prime_annuelle DECIMAL(15,2) DEFAULT 0,
    statut VARCHAR(20) DEFAULT 'en_cours' CHECK (statut IN ('en_cours', 'suspendue', 'resiliee')),
    beneficiaires JSONB DEFAULT '[]',
    documents JSONB DEFAULT '{}',
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index pour polices
CREATE INDEX IF NOT EXISTS idx_polices_numero ON polices(numero_police);
CREATE INDEX IF NOT EXISTS idx_polices_statut ON polices(statut);
CREATE INDEX IF NOT EXISTS idx_polices_type ON polices(type_police);
CREATE INDEX IF NOT EXISTS idx_polices_assure ON polices(assure_principal);
CREATE INDEX IF NOT EXISTS idx_polices_date_creation ON polices(date_creation DESC);

-- =====================================================

-- Table: cotations_excel
-- Stocke les résultats de micro-tarification Excel pour Corporate
CREATE TABLE IF NOT EXISTS cotations_excel (
    id BIGSERIAL PRIMARY KEY,
    numero_devis VARCHAR(50) NOT NULL REFERENCES devis(numero_devis) ON DELETE CASCADE,
    entreprise VARCHAR(200) NOT NULL,
    produit VARCHAR(100) NOT NULL,
    nb_total_lignes INTEGER DEFAULT 0,
    nb_eligibles INTEGER DEFAULT 0,
    nb_exclus INTEGER DEFAULT 0,
    nb_erreurs INTEGER DEFAULT 0,
    prime_nette_totale DECIMAL(15,2) DEFAULT 0,
    prime_ttc_totale DECIMAL(15,2) DEFAULT 0,
    prime_finale DECIMAL(15,2) DEFAULT 0,
    reduction_commerciale DECIMAL(5,2) DEFAULT 0,
    duree_contrat INTEGER DEFAULT 12,
    statut VARCHAR(20) DEFAULT 'En cours' CHECK (statut IN ('En cours', 'Validé', 'Annulé')),
    resultats_detailles JSONB,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_cotations_excel_devis ON cotations_excel(numero_devis);
CREATE INDEX idx_cotations_excel_entreprise ON cotations_excel(entreprise);
CREATE INDEX idx_cotations_excel_date ON cotations_excel(date_creation DESC);

-- =====================================================

-- Table: historique_modifications
-- Piste d'audit pour tracer toutes les modifications
CREATE TABLE IF NOT EXISTS historique_modifications (
    id BIGSERIAL PRIMARY KEY,
    numero_devis VARCHAR(50) NOT NULL,
    type_action VARCHAR(50) NOT NULL,
    champ_modifie VARCHAR(100),
    ancienne_valeur TEXT,
    nouvelle_valeur TEXT,
    utilisateur VARCHAR(100) DEFAULT 'Système',
    date_modification TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Index
CREATE INDEX idx_historique_devis ON historique_modifications(numero_devis);
CREATE INDEX idx_historique_date ON historique_modifications(date_modification DESC);

-- =====================================================

-- Table: utilisateurs (optionnel - pour gestion des accès)
CREATE TABLE IF NOT EXISTS utilisateurs (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    nom_complet VARCHAR(200) NOT NULL,
    role VARCHAR(50) DEFAULT 'Agent' CHECK (role IN ('Admin', 'Manager', 'Agent', 'Consultant')),
    actif BOOLEAN DEFAULT TRUE,
    date_creation TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    derniere_connexion TIMESTAMP WITH TIME ZONE
);

-- Index
CREATE INDEX idx_utilisateurs_email ON utilisateurs(email);
CREATE INDEX idx_utilisateurs_role ON utilisateurs(role);

-- =====================================================

-- TRIGGERS pour mettre à jour automatiquement date_modification

CREATE OR REPLACE FUNCTION update_modified_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.date_modification = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_devis_modtime
    BEFORE UPDATE ON devis
    FOR EACH ROW
    EXECUTE FUNCTION update_modified_column();

-- =====================================================

-- VUES UTILES

-- Vue: statistiques_devis
CREATE OR REPLACE VIEW statistiques_devis AS
SELECT 
    type_marche,
    statut,
    COUNT(*) as nombre_devis,
    SUM(prime_finale) as total_primes,
    AVG(prime_finale) as prime_moyenne,
    MIN(prime_finale) as prime_min,
    MAX(prime_finale) as prime_max
FROM devis
GROUP BY type_marche, statut;

-- Vue: devis_recents
CREATE OR REPLACE VIEW devis_recents AS
SELECT 
    numero_devis,
    type_marche,
    produit,
    COALESCE(nom_client, entreprise) as client,
    prime_finale,
    statut,
    date_creation
FROM devis
ORDER BY date_creation DESC
LIMIT 50;

-- =====================================================

-- POLICIES RLS (Row Level Security) - À adapter selon vos besoins

-- Activer RLS sur les tables sensibles
ALTER TABLE devis ENABLE ROW LEVEL SECURITY;
ALTER TABLE assures ENABLE ROW LEVEL SECURITY;
ALTER TABLE cotations_excel ENABLE ROW LEVEL SECURITY;

-- Politique pour permettre la lecture à tous les utilisateurs authentifiés
CREATE POLICY "Lecture publique pour utilisateurs authentifiés" 
ON devis FOR SELECT 
TO authenticated 
USING (true);

-- Politique pour permettre l'insertion à tous les utilisateurs authentifiés
CREATE POLICY "Insertion pour utilisateurs authentifiés" 
ON devis FOR INSERT 
TO authenticated 
WITH CHECK (true);

-- Répéter pour les autres tables si nécessaire
CREATE POLICY "Lecture publique assures" ON assures FOR SELECT TO authenticated USING (true);
CREATE POLICY "Insertion assures" ON assures FOR INSERT TO authenticated WITH CHECK (true);

CREATE POLICY "Lecture publique cotations" ON cotations_excel FOR SELECT TO authenticated USING (true);
CREATE POLICY "Insertion cotations" ON cotations_excel FOR INSERT TO authenticated WITH CHECK (true);

-- =====================================================
-- FIN DU SCRIPT
-- =====================================================

-- NOTES:
-- 1. Exécutez ce script dans l'éditeur SQL de Supabase
-- 2. Ajustez les policies RLS selon vos besoins de sécurité
-- 3. Les index sont optimisés pour les requêtes fréquentes
-- 4. Les types JSONB permettent la flexibilité pour les données complexes
