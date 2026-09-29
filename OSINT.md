# OSINT for Humanity Loop

Humanity Loop may use open-source intelligence (OSINT) as a scouting, verification, provenance, accountability, and weak-signal capability.

The OSINT4ALL board is a useful **index**, not a whitelist. Tools must be evaluated individually for legality, reliability, ethics, and fit.

## High-value OSINT categories

### 1. Source preservation / historical reconstruction

Use when:
- a page changed or disappeared;
- a regulator silently revised guidance;
- a weak signal existed only briefly;
- we need to establish what was publicly available at a prior date.

Useful tools:
- Wayback Machine — https://web.archive.org/
- archive.is — https://archive.is/
- Oldweb.today — http://oldweb.today/
- waybackpy — https://pypi.org/project/waybackpy/
- Unpaywall — https://unpaywall.org/

Humanity Loop rule: preserve original source URL, capture date, archive URL, and retrieved text/hash where feasible.

### 2. Media/image verification

Use when:
- a weak signal first appears as a photo/video;
- environmental/disaster evidence needs independent verification;
- images may be old, recycled, altered, or context-shifted.

Useful tools:
- TinEye — https://tineye.com/
- Google/Bing/Yandex reverse-image search
- FotoForensics — https://fotoforensics.com/
- Forensically — https://29a.ch/photo-forensics/
- EXIF viewers such as Jimpl / exifdata.com
- DiffChecker image diff — https://www.diffchecker.com/image-diff/

Do not treat any single forensic heuristic as proof of manipulation.

### 3. Narrative / social-signal analysis

Use when:
- detecting emerging narratives, rumors, fear/grievance waves, or public-health misinformation;
- mapping how claims move between communities;
- identifying weak signals before mainstream coverage.

Useful tools:
- OSoMe Network Tool — https://osome.iu.edu/tools/networks/
- OSoMe Trends Tool — https://osome.iu.edu/tools/trends/
- Hoaxy — https://hoaxy.osome.iu.edu/
- Social Searcher — https://www.social-searcher.com/
- Boardreader — https://boardreader.com/
- Milled — https://milled.com/search

Guardrail: analyze aggregate/public discourse; do not turn this into private-person surveillance.

### 4. Corporate / ownership / money-flow accountability

Use when:
- evaluating environmental claims;
- checking ownership networks;
- mapping conflicts of interest;
- investigating shell-company or offshore structures;
- tracing organizations around an intervention.

Useful tools:
- OpenCorporates — https://opencorporates.com/
- ICIJ Offshore Leaks — https://offshoreleaks.icij.org/
- OCCRP data/Aleph — https://data.occrp.org/
- Companies House — https://www.gov.uk/government/organisations/companies-house
- LittleSis — https://littlesis.org/
- ProPublica Nonprofit Explorer — https://projects.propublica.org/nonprofits/
- SEDAR+/issuer filings for Canada
- official securities/corporate registries for the relevant jurisdiction

Guardrail: public-interest entity research is preferred over personal profiling.

### 5. Government / public-record accountability

Use when:
- verifying institutional claims;
- tracing public spending or regulation;
- checking court/legal outcomes;
- locating government records that search engines miss.

Useful tools:
- MuckRock — https://www.muckrock.com/
- CourtListener — https://www.courtlistener.com/
- CanLII — https://www.canlii.org/
- PACER where lawful/appropriate
- official open-data portals
- ProPublica public datasets
- GovQuery connector when available

### 6. Geospatial / environmental / humanitarian intelligence

Use when:
- validating environmental damage;
- scouting coral, wildfire, flood, drought, mining, pollution, land-use, or disaster signals;
- comparing local reports with geospatial evidence.

Useful sources surfaced by the OSINT4ALL board:
- US GeoPlatform — https://www.geoplatform.gov/
- INSPIRE Geoportal — https://inspire-geoportal.ec.europa.eu/
- FAO geospatial/data portals — https://data.apps.fao.org/
- UNEP GRID datasets — https://www.unepgrid.ch/
- ISRIC soil data — https://data.isric.org/
- ArcGIS public layers — https://www.arcgis.com/
- ACLED — https://acleddata.com/
- OpenWeatherMap / historical weather services
- Nextstrain for pathogen evolution — https://nextstrain.org/

Complement these with authoritative satellite/earth-observation sources such as Copernicus, NASA Earthdata, USGS, NOAA, and Global Forest Watch when relevant.

### 7. Multilingual / local-source discovery

Use when:
- weak signals may exist only in local-language media or forums;
- mainstream English-language sources lag behind;
- scouts need region-specific search coverage.

Useful techniques/tools:
- DeepL / Google / Bing / Yandex translation;
- Baidu, Yandex, Mojeek, Brave, regional search engines;
- 2lingual and multilingual search;
- local-language query expansion;
- local archives, universities, NGOs, public agencies, and practitioner forums.

Always preserve original-language text alongside translations for important evidence.

### 8. Technical / scientific discovery

Useful tools on the board:
- Crossref — https://search.crossref.org/
- arXiv — https://arxiv.org/
- bioRxiv — https://www.biorxiv.org/
- Google Scholar
- GitHub/awesome lists
- Wolfram|Alpha
- OSINT Framework — https://osintframework.com/

Humanity Loop should still prefer its specialized installed research stack (Undermind, Scite, Consensus, Amass, Pendar, Lune, SciSpace, etc.) when those are better suited.

## Explicitly excluded by default

Humanity Loop must **not** operationalize these OSINT4ALL categories as normal scouting tools:

- fake identity / fake document generators;
- throwaway phone/SMS/email tools used to impersonate or evade controls;
- leaked-password/breach credential databases for account access;
- hash cracking/recovery against third-party accounts;
- exploit databases or intrusion tooling for unauthorized access;
- face-recognition or people-finding systems used to identify private individuals;
- resident/voter databases for political profiling;
- stalking/doxxing tools;
- shadow libraries/piracy as a credential workaround;
- darknet sources involving illegal acquisition or private-data trading.

Exceptions require a clearly lawful defensive/public-interest purpose, minimal data use, and Humanity Loop governance review.

## OSINT evidence hierarchy

Prefer:
1. primary/official record;
2. archived primary source;
3. reputable public database with provenance;
4. independent secondary verification;
5. social/media weak signal;
6. anonymous/unverified claim.

Weak signals can trigger investigation. They cannot carry a high-impact decision alone.

## Scout workflow

1. Capture the weak signal.
2. Preserve/archival snapshot.
3. Search local-language and regional sources.
4. Search geospatial/media/corporate/public-record evidence as appropriate.
5. Triangulate at least two independent sources for material claims.
6. Record provenance and uncertainty.
7. Pass promising signals to a specialist/verification agent.
8. Log rejected/false signals so future agents learn what failed.

## Source board

OSINT4ALL:
https://start.me/p/L1rEYQ/osint4all
