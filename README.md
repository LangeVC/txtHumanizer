# txtHumanizer

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-blue)](https://github.com/LangeVC/txtHumanizer/releases/tag/v1.0.0)
[![Status](https://img.shields.io/badge/status-production%20ready-green)](https://github.com/LangeVC/txtHumanizer)
[![Capacium](https://img.shields.io/badge/Capacium-0B1020?style=flat-square&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0iI0Y3RkFGQyIgZD0iTTEyIDJDNi40OCAyIDIgNi40OCAyIDEyczQuNDggMTAgMTAgMTAgMTAtNC40OCAxMC0xMFMxNy41MiAyIDEyIDJ6bTAgMThjLTQuNDEgMC04LTMuNTktOC04czMuNTktOCA4LTggOCAzLjU5IDggOC0zLjU5IDgtOCA4em0wLTE0Yy0zLjMxIDAtNiAyLjY5LTYgNnMyLjY5IDYgNiA2IDYtMi42OSA2LTYtMi42OS02LTYtNnoiLz48L3N2Zz4=)](https://github.com/Capacium/capacium)
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
