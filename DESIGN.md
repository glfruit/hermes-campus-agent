# Design System: Hermes Campus Agent

## 1. Visual Theme & Atmosphere

Hermes Campus Agent is a restrained operational workspace for teaching management. It should feel quiet, precise, and trustworthy: a work surface for scanning tasks, reading cited policies, reviewing generated drafts, and moving between Web and WeCom actions.

Use a product register. Design serves repeated work. Avoid decorative AI visuals, oversized hero sections, nested cards, and purple-blue gradient defaults.

Physical scene: a teaching manager reviews weekly teaching operations on a desktop monitor during office hours, with WeCom notifications on mobile for quick follow-up. The UI should support attention, comparison, and fast correction.

## 2. Color Palette & Roles

- Porcelain Warm Gray (#F7F6F2): main app background, slightly warmer than pure white to reduce glare.
- Ink Charcoal (#1F2523): primary text and high-emphasis labels.
- Administrative Green (#2F6F5E): primary actions, source badges, active navigation, and confirmation states.
- Ledger Blue (#315D83): analytical accents, data summaries, and links to reports.
- Review Amber (#A66B18): warnings, pending review, and items requiring confirmation.
- Critical Carmine (#A33A3A): errors, blocked items, and high-risk decisions that require human handling.
- Mist Gray (#E4E1DA): borders, dividers, inactive controls, and table rules.
- Field Stone (#FCFBF8): surfaces for forms, document panels, and source excerpts.

Do not use `#000000` or `#FFFFFF`. Keep saturated color usage below 10% on operational screens. Use color to encode state and role, not decoration.

## 3. Typography Rules

- Use a system Chinese-friendly stack first: `Inter`, `Noto Sans SC`, `PingFang SC`, `Microsoft YaHei`, `system-ui`, sans-serif.
- Body text should be compact and readable at 14px to 15px.
- Operational labels and table headers should use 12px to 13px with medium weight.
- Page headings should stay restrained, usually 20px to 28px.
- Avoid hero-scale typography inside dashboards, sidebars, cards, and tool panels.
- Keep letter spacing at 0 unless using very small all-caps technical labels.

## 4. Component Stylings

- **Buttons:** 6px to 8px radius, clear icon support, primary action in Administrative Green. Destructive actions must use Critical Carmine and require explicit confirmation.
- **Cards and panels:** use cards only for repeated objects, source excerpts, task items, or modals. Do not put cards inside cards.
- **Tables:** support dense scanning with sticky headers, subtle row separators, and status chips.
- **Inputs:** light Field Stone background, Mist Gray border, visible focus ring in Administrative Green.
- **Navigation:** compact left rail or top tabs. Active items should be obvious through color and weight, not oversized shapes.
- **Source citations:** show document title, department, version/date, and confidence/coverage hints near the answer.
- **AI output:** clearly separate draft text, cited facts, assumptions, and required human review.

## 5. Layout Principles

- Default to workbench layouts: navigation, task/context sidebar, main work area, source/detail panel.
- Favor split panes for chat plus citations, or document plus generated draft.
- Keep fixed-format UI elements stable with explicit dimensions and responsive constraints.
- Avoid centered marketing composition after login.
- On mobile WeCom views, present short answers, task summaries, and links back to Web rather than compressing full desktop workflows.

## 6. Do's and Don'ts

Do:

- Make sources, permissions, and review states visible.
- Use compact controls for repeated work.
- Preserve enough whitespace around dense data for readability.
- Treat AI-generated content as draft until confirmed.
- Provide empty states that invite a concrete next action.

Don't:

- Use purple gradients, glassmorphism, bokeh, or decorative AI imagery as a default.
- Hide source citations behind hover-only interactions.
- Make the chat box the only product surface.
- Use color as the only signal for risk or status.
- Let generated text visually resemble an approved official decision.
