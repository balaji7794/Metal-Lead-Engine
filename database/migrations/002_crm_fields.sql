ALTER TABLE companies
ADD COLUMN lead_status TEXT DEFAULT 'New';

ALTER TABLE companies
ADD COLUMN priority TEXT DEFAULT 'Medium';

ALTER TABLE companies
ADD COLUMN last_contacted TEXT;

ALTER TABLE companies
ADD COLUMN next_followup TEXT;

ALTER TABLE companies
ADD COLUMN remarks TEXT;