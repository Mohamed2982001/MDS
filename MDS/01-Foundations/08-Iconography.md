# MDS Foundation: Iconography & RTL Mirroring Specification
**Foundational Layer:** 01-Foundations  
**Status:** APPROVED  
**Lead Architect:** Mohamed Khalid (Senior Full Stack & Flutter Developer)  
**Last Updated:** 2026-09-14  

---

## 1. Iconographic Philosophy & Aesthetic

MDS iconography follows the principles of **geometric precision and subtle tactile softness**:
- **Stroke-First Default:** All standard icons use outlined geometric strokes with rounded caps and joins.
- **Filled for State & Emphasis:** Solid/filled variants are reserved for active navigation tabs, selected toggles, and status badges.
- **Stroke Weight Consistency:** Standard 1.5px stroke on a 20px optical area; 2px stroke on 24px and 32px viewports for optical weight parity.

---

## 2. Standardized Icon Grid & Bounding Box

To maintain visual weight parity across icons of varying silhouettes:
- **Standard Canvas Box:** 24×24px bounding box.
- **Live Optical Area:** 20×20px central drawing area.
- **Padding:** 2px internal safety margin.

---

## 3. Semantic RTL Mirroring Rules Taxonomy

In RTL (Arabic) environments, icon mirroring is governed strictly by semantic meaning, not arbitrary lists:

### Rule 1: Reading & Text Flow Direction $\to$ MIRRORS
Icons that communicate writing direction, list bulleting, or text alignment mirror horizontally to match the right-to-left flow of reading:
- Text alignment indicators (align-left $\leftrightarrow$ align-right)
- List hierarchy markers and bullet indents

### Rule 2: Temporal & Spatial Progression $\to$ MIRRORS
Icons that communicate historical time travel (undo/redo), navigation sequences, or pagination progress mirror with the flow of time/reading:
- Navigation Back / Forward arrows (`arrow-left` $\leftrightarrow$ `arrow-right`)
- Chevrons (`chevron-left` $\leftrightarrow$ `chevron-right`)
- Undo / Redo triggers
- Step-by-step wizard progression meters

### Rule 3: Physical Tool & Real-World Object Invariance $\to$ NEVER MIRRORS
Icons that represent real-world physical objects, hardware tools, or identity concepts remain invariant because physical geometry does not reverse in RTL cultures:
- Search magnifying glass (handle stays pointing down-right)
- Tools: camera, microphone, pencil, wrench, scissors
- Security & identity: lock, key, shield, user avatar, group
- Status marks: checkmark, close/cross, warning triangle, info circle

### Rule 4: International Media Transport Standards $\to$ NEVER MIRRORS
Media playback controls follow international hardware standards (IEC 60417) and remain invariant worldwide:
- Play ($\blacktriangleright$) points right in all languages and regions
- Fast-forward ($\blacktriangleright\blacktriangleright$), Rewind ($\blacktriangleleft\blacktriangleleft$), Pause ($\mathbf{\text{II}}$), Stop ($\blacksquare$)
