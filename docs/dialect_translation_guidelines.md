# German Dialect Translation Guidelines

## Overview

This document provides guidelines for translating MacGyver Multi-Tool UI terms into 38 German dialects. The goal is to balance **authenticity** with **usability** while preserving regional character.

---

## General Principles

### 1. **Authenticity vs. Readability**
- Use genuine dialect terms where they exist
- Avoid overly obscure terms that speakers wouldn't recognize
- Prioritize comprehension over perfect linguistic accuracy

### 2. **Consistency**
- Use consistent spelling conventions within each dialect
- Document decisions in this file
- Create a mini-dictionary for recurring terms

### 3. **UI Context**
- **Menu items**: Clear and concise
- **Buttons**: Action-oriented
- **Tooltips**: Can be more dialect-heavy
- **Error messages**: Prioritize clarity

### 4. **Phonetic Writing**
- Write as spoken, not as Standard German
- Example: "nicht" → "ned" (Bavarian), "net" (Swabian)

### 5. **Preserve Emojis & Markers**
- Keep all emojis (🕰️, 💀, 🔴, 🎭, 🍎, etc.)
- Maintain formatting markers

---

## Dialect-Specific Patterns

### Bavarian (de_bavaria)
**Characteristics**:
- `-en` → `-a` (endings)
- `ei` → `oa` (diphthong shift)
- `nicht` → `ned`
- Diminutive: `-erl` or `-l`

**Examples**:
- Datei → Datoei / Akte
- Einstellungen → Ostellunga
- öffnen → aufmacha

### Swabian (de_swabian)
**Characteristics**:
- `-en` → `-e` or `-a`
- `nicht` → `net`  
- `ich` → `i`
- Softer consonants

**Examples**:
- Datei → Datei (same)
- Einstellungen → Oischtellunge
- öffnen → aufmache

### Saxon (de_saxony)
**Characteristics**:
- `g` → `ch` (often)
- `ei` → `ee`
- Unique vowel shifts
- `-ig` → `-sch`

**Examples**:
- sagen → sachn
- wichtig → wichtsch
- Einstellungen → Oinstellungen

### Kölsch/Ripuarian (de_ripuarian)
**Characteristics**:
- Soft pronunciation
- Rhine Franconian influence
- `-chen` → `-che`
- Many unique words

**Examples**:
- klein → kleen
- Mädchen → Mädche
- nicht → nit

---

## Translation Priority

### Critical (Must Translate)
1. Menu items (File, Edit, Settings, etc.)
2. Dialog buttons (OK, Cancel, Save, etc.)
3. Tab names
4. Widget titles

### Important (Should Translate)
1. Tooltips
2. Status messages
3. Subheadings

### Optional (Can Use Standard German)
1. Long descriptive text
2. Technical terms without dialect equivalents
3. Proper nouns

---

## Research Resources

### Online Dictionaries
- **Bavarian**: https://www.bayerisches-woerterbuch.de/
- **Swabian**: https://www.schwaebisch-schwaetza.de/
- **Kölsch**: https://www.koelsch-woerterbuch.de/
- **General**: Wikipedia dialect articles

### Linguistic References
- Deutscher Sprachatlas (DSA)
- Regional dialect research centers
- University linguistics departments

### Community Sources
- Regional forums and language communities
- Native speaker consultation
- Social media dialect groups

---

## Common UI Term Translations

### Universal Terms (Adapt per dialect)

| English | Standard German | Bavarian | Swabian | Saxon | Kölsch |
|---------|----------------|----------|---------|-------|--------|
| File | Datei | Datoei / Akte | Datei | Datei | Datei |
| Open | Öffnen | Aufmacha | Aufmache | Uffmache | Opmaache |
| Close | Schließen | Zuamacha | Zuemache | Zumache | Zomaache |
| Save | Speichern | Speichern | Speichere | Speichern | Speichere |
| Settings | Einstellungen | Oistellunga | Oischtellunge | Oinstellunge | Enstellunge |
| Help | Hilfe | Huif | Helfe | Hilfe | Hölp |
| Exit | Beenden | Beenda | Beende | Beenden | Ophöre |
| New | Neu | Nei | Nei | Nei | Neu |
| Edit | Bearbeiten | Bearweita | Bearbeite | Bearbeiten | Bearbeide |
| Delete | Löschen | Lösche | Lösche | Läsche | Fottschmieße |
| Cancel | Abbrechen | Obbrecha | Abbräche | Abbrächn | Afbrächhe |
| OK | OK | OK | OK | OK | OK |
| Yes | Ja | Jo | Ja | Ja | Jo |
| No | Nein | Na / Naa | Noi | Nee | Nä |

---

## Quality Checklist

Before finalizing a dialect translation:

- [ ] Does it sound natural when spoken aloud?
- [ ] Would a native speaker understand it immediately?
- [ ] Is it consistent with other terms in the same dialect?
- [ ] Does it maintain the original meaning?
- [ ] Is it appropriate for UI context (not too casual)?
- [ ] Are emojis and markers preserved?
- [ ] Is spelling consistent?

---

## Workflow

### 1. Research Phase
- Gather resources for specific dialect
- Create mini-dictionary of key terms
- Identify patterns

### 2. Translation Phase
- Translate critical terms first
- Use patterns to speed up translation
- Document unique decisions

### 3. Review Phase
- Read aloud to check naturalness
- Cross-check with resources
- Flag uncertain translations for community review

### 4. Integration Phase
- Add to `translation_master.json`
- Generate language file
- Test in UI

---

## Special Cases

### Technical Terms
When no dialect equivalent exists:
1. Use Standard German
2. Add phonetic adaptation if natural
3. Consider loanword adaptation

**Example**: "Monitor" → "Monitor" (all dialects)

### Compound Words
Break down and translate components:
- Standard: "Systemmonitor"
- Bavarian: "Systemmonitor" (keep technical)
- OR: "Systemwachter" (if translating "monitor" as "watcher")

### Humor & Regional Character
- Preserve regional personality
- Avoid offensive stereotypes
- Keep it professional but characterful

---

## Notes for Specific Dialects

### Historical Dialects (💀 markers)
- Use historical sources
- Academic approach
- May be reconstructed/approximated

### Endangered Dialects (🔴 markers)
- Prioritize preservation
- Document sources carefully
- Accept approximations

### Urban Dialects
- Modern slang acceptable
- Reflect contemporary usage
- Balance tradition and modernity

---

## Revision History
- 2025-11-23: Initial guidelines created
- TBD: Updates based on community feedback

---

**Remember**: These are living languages. Community input is essential for quality!
