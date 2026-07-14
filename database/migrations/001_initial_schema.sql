PRAGMA foreign_keys = ON;

-- =====================================================
-- COMPANIES
-- =====================================================

CREATE TABLE IF NOT EXISTS companies (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_code TEXT UNIQUE,

    company_name TEXT NOT NULL,

    google_maps_url TEXT UNIQUE,

    website TEXT,

    phone TEXT,

    email TEXT,

    address TEXT,

    city TEXT,

    state TEXT,

    country TEXT,

    pincode TEXT,

    category TEXT,

    industry_type TEXT,

    business_type TEXT,

    msme_type TEXT,

    products TEXT,

    scrap_generated TEXT,

    estimated_consumption_mt REAL,

    estimated_scrap_mt REAL,

    rating REAL,

    reviews INTEGER,

    source TEXT,

    notes TEXT,

    lead_status TEXT DEFAULT 'New',

    priority TEXT DEFAULT 'Medium',

    last_contacted TEXT,

    next_followup TEXT,

    remarks TEXT,

    status TEXT DEFAULT 'ACTIVE',

    confidence_score REAL,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP

);

-- =====================================================
-- PHONES
-- =====================================================

CREATE TABLE IF NOT EXISTS company_phones (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    phone TEXT,

    phone_type TEXT,

    is_primary INTEGER DEFAULT 0,

    verified INTEGER DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- EMAILS
-- =====================================================

CREATE TABLE IF NOT EXISTS company_emails (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    email TEXT,

    department TEXT,

    is_primary INTEGER DEFAULT 0,

    verified INTEGER DEFAULT 0,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- WEBSITES
-- =====================================================

CREATE TABLE IF NOT EXISTS company_websites (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    website TEXT,

    website_type TEXT,

    is_primary INTEGER DEFAULT 0,

    last_crawled DATETIME,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- PRODUCTS
-- =====================================================

CREATE TABLE IF NOT EXISTS company_products (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    product_name TEXT,

    product_category TEXT,

    grade TEXT,

    confidence REAL,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- SCRAP
-- =====================================================

CREATE TABLE IF NOT EXISTS company_scrap (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    scrap_name TEXT,

    scrap_category TEXT,

    estimated_mt REAL,

    confidence REAL,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- CONTACTS
-- =====================================================

CREATE TABLE IF NOT EXISTS company_contacts (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    person_name TEXT,

    designation TEXT,

    phone TEXT,

    email TEXT,

    linkedin TEXT,

    notes TEXT,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);

-- =====================================================
-- SEARCH HISTORY
-- =====================================================

CREATE TABLE IF NOT EXISTS search_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    keyword TEXT,

    location TEXT,

    radius INTEGER,

    source TEXT,

    results_found INTEGER,

    started_at DATETIME,

    completed_at DATETIME

);

-- =====================================================
-- COMPANY SEARCHES
-- =====================================================

CREATE TABLE IF NOT EXISTS company_searches (

    company_id INTEGER,

    search_id INTEGER,

    PRIMARY KEY(company_id, search_id),

    FOREIGN KEY(company_id) REFERENCES companies(id),

    FOREIGN KEY(search_id) REFERENCES search_history(id)

);

-- =====================================================
-- NOTES
-- =====================================================

CREATE TABLE IF NOT EXISTS company_notes (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    company_id INTEGER NOT NULL,

    note TEXT,

    follow_up_date DATE,

    priority TEXT,

    status TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(company_id) REFERENCES companies(id)

);