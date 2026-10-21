# txtHumanizer

[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-0.4.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v0.4.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-Install%20via%20cap-0B1020?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MTYuNzQiIGhlaWdodD0iNjE2Ljc0IiB2aWV3Qm94PSIwIDAgNjE2Ljc0IDYxNi43NCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmN2ZhZmN9PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTAgMGg2MTYuNzR2NjE2Ljc0SDB6Ii8+PHBhdGggaWQ9IkViZW5lXzIiIGQ9Ik0wIDBoNjE2Ljc0djYxNi43NEgweiIgZGF0YS1uYW1lPSJFYmVuZSAyIiBzdHlsZT0iZmlsbDojMGIxMDIwIi8+PGcgaWQ9IkViZW5lXzEiIGRhdGEtbmFtZT0iRWJlbmUgMSI+PHBhdGggZD0ibTMwOC44MyA1OTAuNDctMzYuMDItMzYuMjQtMjExLjMyLS4wNC0uMDItMjExLjczLTMzLjExLTMzLjk3IDMzLjEtMzIuODMuMDYtMjE1Ljc0IDIxMy43NC0uMDQgMzMuNDQtMzIuOTcgMzIuNzIgMzIuOTUgMjE0LjAxLjA2LjA5IDIxNS42MiAzMi44NSAzMi43Ni0zMi45OCAzMy4xMS4wNyAyMTIuNzQtMjEwLjQuMTItMzYuMjMgMzYuMjJabS4yMy0zNi4wOSA3NS41OS03Ni44NCAxMzkuODMtMTQxLjMxIDI3LjcxLTI4LjE2LTkwLjY1LTkwLjcyTDMwOC4zMiA2NC4yMSAxODYuOCAxODQuNzVsLTk0LjkzIDk1LjQ2LTI4LjEyIDI4LjQ0IDEwNC43NSAxMDUuNSA3NC4wOCA3My42NnptLTkxLjgtNDM1Ljk0IDMyLjE0LTMyLjAyLTE2Mi41MS0uMDMuMDQgMTYyLjQ4em0zMTIuNjMtMzIuMDgtMTYyLjY1LjA2TDUyOS44NSAyNDguOXptLTMxNy4zIDQwOC4xMi04MC41NS04MS44Ny00NS4wMi00NS43Mi0uMTEgMTYyLjA2IDE1OS40Ny0uMDV6bTE1NS43NiAzNC40NmgxNjEuNTNsLS4wNS0xNjIuMDQtNTUuMSA1NC45OXoiIGNsYXNzPSJjbHMtMSIvPjxwYXRoIGQ9Im0zMDguODIgNDgwLjA3LTc5Ljc3LTQ3LjczLTY3LjEyLTQwLjA3LS4wMi0xNzAuNzMgMTQ2LjcyLTg0LjI1IDY0LjgzIDM2Ljg1IDgyLjkyIDQ3LjE1LjAyIDE3MS40OC0xNDcuNTkgODcuM1ptMTcuNzctMjQ4LjUzYzE2LjA4IDQuMzYgMjkuNzMgMTMuMzggNDAuNDcgMjYuMTZsNDkuNTktMjguNDktMTA3Ljc4LTYyLjgxLTEwNy4xNyA2Mi40MyA0OS43NSAyOC41NWMxOC4yNi0yMi42NiA0Ni45OS0zMi44NCA3NS4xNS0yNS44NFptLTMwLjc3IDE1NC45MmMtNDcuNTktMTAuMjEtNzQuOTYtNjAuODMtNTcuMTgtMTA2LjM5bC01MC45LTI5LjYxLS4wOCAxMjguNCAxMDguMDYgNjIuMzIuMS01NC43Wm0yNi4xMy4xNC4yOCA1NC42NCAxMDcuOS02Mi4yOS0uMDUtMTI4LjI0LTQ5Ljc0IDI5LjI3YTc5LjI1IDc5LjI1IDAgMCAxLTMxLjM5IDk1LjczYy04LjMyIDUuNzEtMTcuMTggOC44Ni0yNi45OSAxMC44OFoiIGNsYXNzPSJjbHMtMSIvPjwvZz48L3N2Zz4=&labelColor=0B1020&logoColor=F7FAFC)](https://github.com/Capacium/capacium)
[![CI](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml)

Modulares, mehrsprachiges und varietätensensitives KI-Erkennungs- und
Humanisierungs-Framework inklusive vollwertiger **Terminal-CLI**. Erkennt und entfernt
KI-typische Muster evidenzbasiert nach den aktuellen Richtlinien von **Wikipedia DE**
(*Anzeichen für KI-generierte Inhalte*) und **Wikipedia EN** (*Signs of AI writing / WP:AISIGNS*).

---

## ⚡ CLI Quickstart

Das Framework enthält eine eigenständige, superschnelle CLI (**0 Abhängigkeiten**, reine Python 3 Standardbibliothek):

```bash
# Direkt ausführen
./bin/txt-humanizer --help

# Oder im Python-Pfad installieren
pip install -e .
```

### Die 6 CLI-Befehle

```bash
# 1. Sprache, Varietät (de-CH, en-GB etc.) & Dialekt erkennen
txt-humanizer detect "Wir parkieren das Velo beim Spital und essen ein bisserl was."

# 2. Text evidenzbasiert prüfen (Score & Belege)
txt-humanizer check draft.md

# 3. CI/CD Gate: Verhindert Commits bei hohem KI-Score (Exit-Code 1)
txt-humanizer check draft.md --fail-on suspect -q

# 4. Rekursiver Verzeichnis-Scan mit Zusammenfassungstabelle
txt-humanizer scan ./docs/ --ext md,txt --report-file scan-report.json

# 5. Regelbasierte Transformation mit farbigem Diff anzeigen
txt-humanizer transform article.md --diff

# 6. Kriterienkatalog und Trigger-Wörter inspizieren
txt-humanizer rules --lang de --tier 1

# 7. Lokalen Git Pre-Commit Hook einrichten
txt-humanizer init-hook
```

### Piping & Agent-Integration (Zero Tokens)
```bash
# Stdin-Piping
cat document.txt | txt-humanizer check - --format json

# Für Coding-Agenten (Claude Code, Antigravity, OpenCode):
txt-humanizer check input.txt -j
```

---

## Installation via Capacium (AI-Agent Skill)

```
ANALYSE (Tier 1-3) → RECOMMEND → FINETUNE
```

### Highlights in v0.3.0
* **Multilingual:** Vollständige Unterstützung für Deutsch (`de`) und Englisch (`en`), modular erweiterbar via YAML-Kataloge.
* **Varietäten- & Dialektschutz:**
  * **DACH:** Bundesdeutsch (`de-DE`), Österreichisches Deutsch (`de-AT`: Austriazismen), Schweizer Hochdeutsch (`de-CH`: Helvetismen, kein *ß*). Regionale Normen sind vor Falsch-Positiven geschützt.
  * **Englisch:** Amerikanisches (`en-US`) vs. Britisches Englisch (`en-GB`). Erkennung von inkonsistentem *Style Bleed* (z. B. UK-Rechtschreibung mit US-Puffery).
  * **Dialekte & Regiolekte:** Bairisch, Alemannisch, Kölsch, Plattdeutsch. Authentische Dialektmerkmale gelten als **positive menschliche Signale** (Human Signals) und senken den KI-Score.
* **Dreistufiges Gewichtungsmodell:** Tier 1 (Harte Belege, 1.0), Tier 2 (Starke Stil-Muster, 0.5), Tier 3 (Schwache Signale, 0.15) mit historischen Decay-Faktoren (z. B. Em-Dash-Abwertung).
* **Automatischer Detektor:** Deterministische Erkennung von Sprache und Varietät in < 20ms (`catalog/engine/detector.py`).
* **Modulare Katalogstruktur:** Alle Regeln liegen sauber getrennt unter `catalog/core/` und `catalog/languages/`.

> **Repository provenance.** The canonical home of this repository is Forgejo at
> `git.langevc.com/langevc/txt-humanizer`. The GitHub repository is a mirror.

```
ANALYSE → RECOMMEND → FINETUNE
```

## Quickstart

### Via Capacium (Recommended)

```bash
# Install Capacium
brew install capacium/tap/capacium

# Install txtHumanizer
cap install LangeVC/txtHumanizer
```

### Via Git (Alternative)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/LangeVC/txtHumanizer.git ~/.claude/skills/txtHumanizer
```

### Via npx skills

```bash
npx skills add LangeVC/txtHumanizer
```

## Usage

```
/humanizer [Text einfügen]
```

Oder direkt:

```
Bitte humanize diesen Text: [dein Text]
```

## Betriebsmodi

txtHumanizer unterstützt ab v0.0.2 zwei Nutzungsarten.

### Automatikmodus

Wenn kein Modusparameter angegeben ist, läuft der Skill im Automatikmodus.
Er führt Analyse, Empfehlungen und Finetune in einem Durchlauf aus.

Fehlende Stil-Regler werden aus dem Ausgangstext abgeleitet. Die gewählte
Konfiguration wird immer offengelegt und kurz begründet.

Beispiel:

```text
[$txtHumanizer]

Hier ist mein Artikel:
...
```

Typische Ausgabe:

```text
=== MODUS ===
Automatik

=== AUTOMATISCHE STILWAHL ===
Domäne: business
Formalität: informell
...

=== BEGRÜNDUNG DER STILWAHL ===
[Ableitung aus Textmerkmalen]
```

### Guide-Modus

Der Guide-Modus führt schrittweise durch den Prozess und stoppt nach den
Hauptstufen. Aktiviert wird er über Parameter oder Formulierungen wie:

```text
guide
guided
geführt
schrittweise
stepwise
interactive
```

Beispiel:

```text
[$txtHumanizer guide]

Hier ist mein Artikel:
...
```

Ablauf:

1. Analyse ausgeben
2. Fortsetzung zu Empfehlungen bestätigen
3. Empfehlungen ausgeben
4. Stil-Regler einzeln auswählen
5. Finetune direkt ausführen, erst planen, überspringen oder Konfiguration ändern

Jeder der sieben Stil-Regler wird als einfache Single-Choice-Frage mit
Custom-Option abgefragt.

## Die drei Stufen

| Stufe | Funktion | Beschreibung |
|---|---|---|
| **1. ANALYSE** | Erkennung | Evidenzbasierte KI-Muster-Erkennung mit Punktesystem (0–10) + Longlist (A1–D4) |
| **2. RECOMMEND** | Empfehlung | Belegbasierte Änderungsempfehlungen pro Kriterium mit vorher/nachher |
| **3. FINETUNE** | Überarbeitung | Zielgerichtete Anwendung mit 7 konfigurierbaren Stil-Reglern |

## Stil-Regler

| Regler | Optionen |
|---|---|
| **Domäne** | alltag, business, akademisch, journalistisch, literarisch, technisch |
| **Formalität** | formell, neutral, informell |
| **Persönlichkeit** | nüchtern, moderat, ausdrucksstark |
| **Texttreue** | konservativ, ausgewogen, mutig |
| **Satzbau** | minimal, moderat, maximal |
| **Kreativität** | standard, kreativ, experimentell |
| **Seele** | keine, leicht, stark |

## Kriterienkatalog

### Schnelltest (10 Kriterien)

| # | Kriterium | Beschreibung |
|---|---|---|
| K1 | Glatte Einleitung | Formelhafte Eröffnung ohne spezifische Fakten |
| K2 | Metafloskeln | „Es ist wichtig zu betonen …" |
| K3 | Konnektoren-Inflation | „darüber hinaus", „zudem", „folglich" gehäuft |
| K4 | Gleichförmiger Satzrhythmus | Gleiche Satzlängen und Strukturen |
| K5 | Dreierlisten | „X, Y und Z" als Standardmuster |
| K6 | „Nicht nur … sondern auch" | Schema­tische Verstärkungsstruktur |
| K7 | Vage Zuschreibungen | „Experten sagen", „Studien zeigen" ohne Quelle |
| K8 | Standard-Abschnitte | „Herausforderungen", „Zukunftsperspektiven" |
| K9 | Gleichförmige Absätze | 3–5 Sätze pro Absatz, identisch aufgebaut |
| K10 | Zu perfekte Übergänge | Didaktisch geglättete Absatzverknüpfungen |

### Deutsche Spezifika (4 Zusatzkriterien)

| # | Kriterium | Beschreibung |
|---|---|---|
| K11 | Anglizismen/Denglisch | „Sinn machen", „in 2024", übermäßige -ieren-Verben |
| K12 | Nominalstil | Extrem verdichtete Nominalphrasen |
| K13 | Partizipialkonstruktionen | Gehäufte „-end"-Formen |
| K14 | KI-Vokabular (DE) | „entscheidend", „vielschichtig", „tiefgreifend" |

### Longlist (optional, 29 Kriterien A1–D4)

Tiefenprüfung nach der deutschen Wikipedia-Longlist — Qualitätsprobleme (A),
stilistische Merkmale (B–C), Hinweise auf menschliche Erstellung (D).

## Beispiel

**Vorher (KI-generiert):**
> Künstliche Intelligenz ist ein bedeutendes und vielschichtiges Themenfeld,
> das in den letzten Jahren zunehmend an Bedeutung gewonnen hat. Es ist wichtig
> zu betonen, dass KI nicht nur die Art und Weise, wie Unternehmen arbeiten,
> grundlegend verändert, sondern auch tiefgreifende Auswirkungen auf die
> Gesellschaft als Ganzes hat. Darüber hinaus zeigen Studien, dass der Einsatz
> von KI-Technologien zu einer signifikanten Steigerung der Effizienz,
> Produktivität und Innovationskraft führen kann.

**Nachher (humanisiert, Modus: business):**
> KI verändert Unternehmensabläufe spürbar. Ein Werkzeugbauer aus Baden-
> Württemberg hat 2024 seine Fertigungsplanung auf ein KI-System umgestellt
> und die Durchlaufzeit um 23 Prozent gesenkt. Ähnliches berichten Logistiker:
> KI-gestützte Routenplanung spart im Schnitt 15 Prozent Kraftstoff.

### Englischer Kriterienkatalog (WP:AISIGNS)

| # | Kriterium | Beschreibung |
|---|---|---|
| EN-PUFFERY | Inflated Symbolism | „pivotal role", „watershed moment", „testament to", „beacon" |
| EN-AI-VOCAB | AI Vocabulary Density | „delve", „tapestry", „foster", „intricate", „spearhead" |
| EN-SUPERFICIAL | Superficial Participles | Satzend-Floskeln mit „-ing" („highlighting the importance of") |
| EN-COPULA-AVOID | Copula Avoidance | „serves as a", „acts as a" statt schlichtem „is" / „are" |
| EN-RULE-OF-THREE | Formulaic Triads | Starre Dreierlisten von Adjektiven oder Phrasen |
| EN-NEG-PARALLEL | Negative Parallelisms | „Not only... but also" Schemata |
| EN-HEDGING | Canned Hedging | „It is worth noting that...", „It is important to remember" |

### Modulare Katalogarchitektur (`catalog/`)

```text
catalog/
├── core/
│   └── meta.yaml               # Tier-Definitionen (1-3), Scoring & Human Signals
├── engine/
│   └── detector.py             # Deterministischer Sprach- & Varietätendetektor
└── languages/
    ├── de/
    │   ├── criteria.yaml       # K1-K14 + Longlist A1-D4 mit Tiering & Decay
    │   ├── transforms.yaml     # Deutsche Transformationsregeln
    │   └── varieties/
    │       ├── de-DE.yaml      # Bundesdeutsch
    │       ├── de-AT.yaml      # Österreichisches Deutsch (Austriazismen)
    │       ├── de-CH.yaml      # Schweizer Hochdeutsch (Helvetismen, kein ß)
    │       └── dialects.yaml   # Bairisch, Alemannisch, Kölsch, Platt (Human Signals)
    └── en/
        ├── criteria.yaml       # WP:AISIGNS Kriterien
        ├── transforms.yaml     # Englische Transformationsregeln
        └── varieties/
            ├── en-US.yaml      # Amerikanisches Englisch
            └── en-GB.yaml      # Britisches Englisch & Style-Bleed-Erkennung
```

## Referenzen

- [Wikipedia:WikiProjekt KI und Wikipedia/Schnelltest KI (v1.35)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Schnelltest_KI)
- [Wikipedia:WikiProjekt KI und Wikipedia/Erkennung KI-Einsatz (Longlist)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Erkennung_KI-Einsatz)
- [Wikipedia:Signs of AI writing (en)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Humanizer Skill by @blader](https://github.com/davila7/claude-code-templates)
- [Capacium – Capability Packaging System](https://github.com/Capacium/capacium)

## Lizenz

Apache-2.0
