# Design Document

## Design Principles
1. **Premium Editorial Feel:** The application should look like a high-end publication crossed with a modern workspace.
2. **Evidence First:** UI must prioritize showing the sources and grounding of every claim.
3. **Restraint:** Avoid gimmicky AI UI patterns (no purple glowing gradients, no excessive glassmorphism).

## Visual Language
- **Typography:**
  - **Inter (Sans-serif):** Used for all UI elements, buttons, inputs, and general body text.
  - **Newsreader (Serif):** Used for editorial headlines, large titles, and empty state heroic text.
- **Color Palette:**
  - **Background:** `#faf9f7` (Warm Off-White) - Soft on the eyes, feels like premium paper.
  - **Surface:** `#ffffff` (White) - Used for cards and message bubbles to pop off the background.
  - **Text Primary:** `#1a1a1a` (Almost Black) - High contrast, extremely legible.
  - **Accent:** `#c45d35` (Warm Terra Cotta) - Distinctive, non-generic accent color.
  - **Sidebar Background:** `#1a1a1a` - Creates a strong architectural split in the layout.

## Information Architecture
- **Left Panel (Sidebar):** Navigation, Session History, Knowledge Library trigger.
- **Center Panel (Chat):** The main conversational interface.
- **Right Panel (Artifact Viewer):** Contextual workspace that only appears when an artifact (Plan, Essay) is generated.

## Main Flows
1. **Empty State:** Greets the user with a massive, confident headline and 4 distinct, action-oriented prompt cards.
2. **Grounded Answer:** When an answer is generated, it is immediately followed by a "HOW THIS ANSWER WAS BUILT" transparency card, and 1-4 Evidence Source cards.
3. **Artifact Generation:** If a user asks for a plan or Ship 30 essay, the right panel slides in, showing the rendered Markdown or HTML.

## Accessibility
- High contrast text (WCAG AA compliant).
- Semantic HTML (`<nav>`, `<main>`, `<article>`).
- Keyboard navigable (focus rings explicitly styled).
