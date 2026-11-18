-- NutriScan bilgi tabanı — okuma modeli (ÖNERİ, 18 Kasım 2026)
-- Bu tablolar data/ altındaki dosyalardan `kb build` ile üretilir; elle yazılmaz.
-- Etiket metni, besin değerleri, profil ve analiz sonucu için tablo YOKTUR (K1, NFR-4).

CREATE TABLE kb_version (
  id                text PRIMARY KEY,                 -- ör. 'kb-2026-11-25-a1b2c3d4'
  git_commit        text NOT NULL,
  content_sha256    text NOT NULL,
  built_at          timestamptz NOT NULL DEFAULT now(),
  active_rule_count integer NOT NULL
);

CREATE TABLE source (
  id            text PRIMARY KEY,                     -- ör. 'eu-1169-2011'
  title         text NOT NULL,
  url           text,
  version_date  date,
  license       text NOT NULL CHECK (license <> '' AND license <> '[..]'),
  license_status text NOT NULL CHECK (license_status IN ('dogrulandi','arastirma_kullanimi')),
  fields_taken  text NOT NULL,
  source_type   text NOT NULL CHECK (source_type IN
                ('regulation','clinical_guideline','efsa_opinion','taxonomy','database','team_decision'))
);

CREATE TABLE concept (
  id         text PRIMARY KEY,                        -- 'en:wheat', 'E102'
  type       text NOT NULL CHECK (type IN
             ('gida_kavrami','katki_maddesi','katki_sinifi')),
  name_tr    text,
  name_en    text,
  e_number   text,
  cas        text,
  mesh_id    text,
  wikidata   text,
  source_id  text NOT NULL REFERENCES source(id)
);

CREATE TABLE concept_parent (                         -- IS_A; döngü kontrolü kb validate'te
  concept_id text NOT NULL REFERENCES concept(id),
  parent_id  text NOT NULL REFERENCES concept(id),
  PRIMARY KEY (concept_id, parent_id),
  CHECK (concept_id <> parent_id)
);

CREATE TABLE alias (
  id          text PRIMARY KEY,                       -- sha1(concept_id|text), Qdrant nokta kimliğiyle aynı
  concept_id  text NOT NULL REFERENCES concept(id),
  text        text NOT NULL,
  text_norm   text NOT NULL,                          -- C3 normalize() çıktısı
  lang        text NOT NULL CHECK (lang IN ('tr','en')),
  relation    text NOT NULL CHECK (relation IN ('SAME_AS','CONTEXTUAL','IS_A','CONTAINS','MAY_CONTAIN')),
  source_id   text NOT NULL REFERENCES source(id),
  status      text NOT NULL CHECK (status IN ('active','draft','retired')),
  reviewer_1  text,
  reviewer_2  text,
  CHECK (status <> 'active' OR source_id NOT LIKE 'team-%'
         OR (reviewer_1 IS NOT NULL AND reviewer_2 IS NOT NULL AND reviewer_1 <> reviewer_2))
);
CREATE INDEX alias_text_norm_idx ON alias (text_norm) WHERE status = 'active';

CREATE TABLE condition (
  id                  text PRIMARY KEY,               -- 'colyak'
  name_tr             text NOT NULL,
  mesh_id             text,
  coverage_note_tr    text NOT NULL,
  required_nutrition  text[] NOT NULL DEFAULT '{}'
);

CREATE TABLE rule (
  id              text NOT NULL,                      -- 'CEL-01'
  version         integer NOT NULL,
  condition_id    text NOT NULL REFERENCES condition(id),
  rule_type       text NOT NULL CHECK (rule_type IN
                  ('varlik','icerebilir','beyan','miktar','eksik_veri','varsayilan')),
  targets         text[] NOT NULL DEFAULT '{}',       -- kavram kimlikleri, beyan kodu ya da besin alanı
  exemptions      text[] NOT NULL DEFAULT '{}',
  bands           jsonb,                              -- miktar: {"kati":[[0.5,"Engel bulunmadı"],...,[null,"Dikkat"]], "sivi":[...]} ya da {"her_ikisi":[...]}
  depends_on_none text[] NOT NULL DEFAULT '{}',       -- yalnız bu kurallar tetiklenmediyse
  outcome         text CHECK (outcome IN ('Uygun değil','Dikkat','Engel bulunmadı','Doğrulanamadı')),
  description_tr  text NOT NULL,
  source_id       text NOT NULL REFERENCES source(id),
  source_section  text,
  source_kind     text NOT NULL CHECK (source_kind IN ('mevzuat','klinik_kilavuz','efsa_gorusu','ekip_karari')),
  status          text NOT NULL CHECK (status IN ('taslak','etkin','emekli')),
  author          text NOT NULL,
  reviewer_1      text,
  reviewer_2      text,
  reviewed_on     date,
  PRIMARY KEY (id, version),
  -- K6: etkin satır iki farklı inceleyici ister, ikisi de yazardan farklı
  CHECK (status <> 'etkin' OR (reviewer_1 IS NOT NULL AND reviewer_2 IS NOT NULL
         AND reviewer_1 <> reviewer_2 AND reviewer_1 <> author AND reviewer_2 <> author
         AND reviewed_on IS NOT NULL)),
  CHECK (rule_type <> 'miktar' OR bands IS NOT NULL),
  CHECK (rule_type = 'miktar' OR outcome IS NOT NULL)
);
-- Her kural kimliğinin en fazla bir etkin sürümü olur
CREATE UNIQUE INDEX rule_one_active_version ON rule (id) WHERE status = 'etkin';

CREATE TABLE derived_field (
  field      text PRIMARY KEY,                        -- 'sodyum_g_100' (API: sodium_g)
  from_field text NOT NULL,                           -- 'tuz_g_100'  (API: salt_g)
  divisor    numeric NOT NULL,                        -- 2.5
  source_id  text NOT NULL REFERENCES source(id)
);

CREATE TABLE evidence (                               -- yalnız araştırma bilgisi; sonuç üretmez (K5)
  concept_id     text NOT NULL REFERENCES concept(id),
  condition_id   text NOT NULL REFERENCES condition(id),
  source         text NOT NULL CHECK (source IN ('CTD','JECFA')),
  relation       text NOT NULL,
  study_count    integer,
  url            text,
  source_version text NOT NULL,
  PRIMARY KEY (concept_id, condition_id, source, relation)
);

CREATE TABLE allergen_group (                         -- TGK alerjen grupları, bilgi alanı (K2)
  id        text PRIMARY KEY,
  name_tr   text NOT NULL,
  source_id text NOT NULL REFERENCES source(id)
);
CREATE TABLE allergen_group_concept (
  group_id   text NOT NULL REFERENCES allergen_group(id),
  concept_id text NOT NULL REFERENCES concept(id),
  PRIMARY KEY (group_id, concept_id)
);

-- Servisin okuduğu görünüm: yalnız etkin kurallar
CREATE VIEW active_rule AS SELECT * FROM rule WHERE status = 'etkin';
