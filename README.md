# txtHumanizer

Drei-Stufen-Humanizer für deutschsprachige Texte. Erkennt und entfernt KI-typische
Muster auf Basis der **Wikipedia KI-Erkennung – Systemkonfiguration v1.35**.

## Installation

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/LangeVC/txtHumanizer.git ~/.claude/skills/txtHumanizer
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
| **1. ANALYSE** | Erkennung | Evidenzbasierte KI-Muster-Erkennung mit Punktesystem (0–10) |
| **2. RECOMMEND** | Empfehlung | Konkrete, belegbasierte Änderungsempfehlungen pro Kriterium |
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

## Lizenz

MIT
