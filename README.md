# txtHumanizer

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v1.0.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-Install%20via%20cap-0B1020?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSI2MTYuNzQiIGhlaWdodD0iNjE2Ljc0IiB2aWV3Qm94PSIwIDAgNjE2Ljc0IDYxNi43NCI+PGRlZnM+PHN0eWxlPi5jbHMtMXtmaWxsOiNmN2ZhZmN9PC9zdHlsZT48L2RlZnM+PHBhdGggZD0iTTAgMGg2MTYuNzR2NjE2Ljc0SDB6Ii8+PHBhdGggaWQ9IkViZW5lXzIiIGQ9Ik0wIDBoNjE2Ljc0djYxNi43NEgweiIgZGF0YS1uYW1lPSJFYmVuZSAyIiBzdHlsZT0iZmlsbDojMGIxMDIwIi8+PGcgaWQ9IkViZW5lXzEiIGRhdGEtbmFtZT0iRWJlbmUgMSI+PHBhdGggZD0ibTMwOC44MyA1OTAuNDctMzYuMDItMzYuMjQtMjExLjMyLS4wNC0uMDItMjExLjczLTMzLjExLTMzLjk3IDMzLjEtMzIuODMuMDYtMjE1Ljc0IDIxMy43NC0uMDQgMzMuNDQtMzIuOTcgMzIuNzIgMzIuOTUgMjE0LjAxLjA2LjA5IDIxNS42MiAzMi44NSAzMi43Ni0zMi45OCAzMy4xMS4wNyAyMTIuNzQtMjEwLjQuMTItMzYuMjMgMzYuMjJabS4yMy0zNi4wOSA3NS41OS03Ni44NCAxMzkuODMtMTQxLjMxIDI3LjcxLTI4LjE2LTkwLjY1LTkwLjcyTDMwOC4zMiA2NC4yMSAxODYuOCAxODQuNzVsLTk0LjkzIDk1LjQ2LTI4LjEyIDI4LjQ0IDEwNC43NSAxMDUuNSA3NC4wOCA3My42NnptLTkxLjgtNDM1Ljk0IDMyLjE0LTMyLjAyLTE2Mi41MS0uMDMuMDQgMTYyLjQ4em0zMTIuNjMtMzIuMDgtMTYyLjY1LjA2TDUyOS44NSAyNDguOXptLTMxNy4zIDQwOC4xMi04MC41NS04MS44Ny00NS4wMi00NS43Mi0uMTEgMTYyLjA2IDE1OS40Ny0uMDV6bTE1NS43NiAzNC40NmgxNjEuNTNsLS4wNS0xNjIuMDQtNTUuMSA1NC45OXoiIGNsYXNzPSJjbHMtMSIvPjxwYXRoIGQ9Im0zMDguODIgNDgwLjA3LTc5Ljc3LTQ3LjczLTY3LjEyLTQwLjA3LS4wMi0xNzAuNzMgMTQ2LjcyLTg0LjI1IDY0LjgzIDM2Ljg1IDgyLjkyIDQ3LjE1LjAyIDE3MS40OC0xNDcuNTkgODcuM1ptMTcuNzctMjQ4LjUzYzE2LjA4IDQuMzYgMjkuNzMgMTMuMzggNDAuNDcgMjYuMTZsNDkuNTktMjguNDktMTA3Ljc4LTYyLjgxLTEwNy4xNyA2Mi40MyA0OS43NSAyOC41NWMxOC4yNi0yMi42NiA0Ni45OS0zMi44NCA3NS4xNS0yNS44NFptLTMwLjc3IDE1NC45MmMtNDcuNTktMTAuMjEtNzQuOTYtNjAuODMtNTcuMTgtMTA2LjM5bC01MC45LTI5LjYxLS4wOCAxMjguNCAxMDguMDYgNjIuMzIuMS01NC43Wm0yNi4xMy4xNC4yOCA1NC42NCAxMDcuOS02Mi4yOS0uMDUtMTI4LjI0LTQ5Ljc0IDI5LjI3YTc5LjI1IDc5LjI1IDAgMCAxLTMxLjM5IDk1LjczYy04LjMyIDUuNzEtMTcuMTggOC44Ni0yNi45OSAxMC44OFoiIGNsYXNzPSJjbHMtMSIvPjwvZz48L3N2Zz4=&labelColor=0B1020&logoColor=F7FAFC)](https://github.com/Capacium/capacium)
[![CI](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml/badge.svg)](https://github.com/LangeVC/txtHumanizer/actions/workflows/ci.yml)
[![Validate](https://img.shields.io/badge/Capacium-Validate-0B1020.svg)](https://github.com/Capacium/capacium-action-validate)
[![Publish](https://img.shields.io/badge/Capacium-Publish-0B1020.svg)](https://github.com/Capacium/capacium-action-publish)

Drei-Stufen-Humanizer für deutschsprachige Texte. Erkennt und entfernt KI-typische
Muster auf Basis der **Wikipedia KI-Erkennung – Systemkonfiguration v1.35**.

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

## Referenzen

- [Wikipedia:WikiProjekt KI und Wikipedia/Schnelltest KI (v1.35)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Schnelltest_KI)
- [Wikipedia:WikiProjekt KI und Wikipedia/Erkennung KI-Einsatz (Longlist)](https://de.wikipedia.org/wiki/Wikipedia:WikiProjekt_KI_und_Wikipedia/Erkennung_KI-Einsatz)
- [Wikipedia:Signs of AI writing (en)](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- [Humanizer Skill by @blader](https://github.com/davila7/claude-code-templates)
- [Capacium – Capability Packaging System](https://github.com/Capacium/capacium)

## Lizenz

MIT
