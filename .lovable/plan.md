# SafeStep bilingual refinement plan

## Goal
Make SafeStep fully usable in English and conversational Hindi, then complete the requested login, practice, glossary quiz, and weekly recap refinements without rebuilding the app.

## 1. Add one app-wide language system
- Add a lightweight React language provider at the root so every screen and shared overlay reads the same `English` / `हिंदी` choice.
- Persist the choice in browser storage and restore it after refresh without causing a mismatched first render.
- Make the language controls on the landing page, login, and My Account update the same global choice instantly.
- Update the document language and apply Noto Sans Devanagari automatically in Hindi mode while retaining Inter for English.
- Centralize shared interface translations and bilingual mock content instead of duplicating strings inside screens.

## 2. Localize every visible experience
- Translate the landing page, login flow, sidebar, help overlay, Home, Ask Before You Click, Learn a Word, Practice, Weekly Recap, Assistant, My Account, reusable feedback, accessibility labels, empty states, and narrow-screen notice.
- Add the supplied Hindi names, definitions, examples, and safety guidance for all eight glossary terms.
- Translate all seven final scenarios in an everyday, family-style Hindi register, including titles, prompts, choices, feedback, and badge names.
- Translate all 40 glossary quiz questions, choices, feedback, and supporting labels while preserving the exact meaning of the supplied English copy.
- Keep SafeStep, numbers, and fixed A/B choice markers unchanged.

## 3. Finish the login experience
- Preserve the two-column presentation and add the SafeStep mark plus a working top-right language switcher.
- Use a fixed `+91` prefix, accept only ten phone digits, keep Send Code disabled until valid, and add the privacy reassurance.
- Add “Step 2 of 2,” six auto-advancing inputs with backspace/paste support, a 30-second resend countdown, and the expandable code explanation.
- On incomplete verification, gently shake the code row once and show the calm validation message; valid verification continues to Home.

## 4. Refine scenario practice and activity tracking
- Use the final seven scenarios: Bank Call, Grandson Emergency, Delivery Message, Shop QR Code, Free Computer Help, Investment Group, and Police Video Call.
- Reuse one shared feedback-card component for scenarios and glossary quizzes: green affirmation for correct answers; amber “Let’s look closer,” consequence explanation, expandable safer choice, and reassurance for incorrect answers.
- Award badges only for correct answers; incorrect answers end with encouragement and a direct way to try another scenario.
- Persist scenario attempts, including whether each scenario was correct on the first try or understood after the reveal, for the recap narrative.

## 5. Expand Learn a Word
- Extend every term with an outlined teal/amber “What it can look like” visual and a 2–3 item “Remember this” list.
- Add a five-question carousel per term as the final modal section, one question at a time, with tappable A/B choices and the shared feedback card.
- Add five clickable progress dots for revisiting questions, reveal “Next question” only after feedback, and finish with the warm closing message plus Back to word list.
- Keep the modal dismissible at any point, reset quiz state sensibly when changing terms, and record viewed term IDs for recap personalization.

## 6. Turn Weekly Recap into a story
- Restyle the two existing counts as achievement cards with larger outlined illustrations.
- Replace plain activity dots with seven labeled day markers that distinguish message checks and scenario practice.
- Add a bilingual “Your Week in Review” narrative informed by first-try versus learned-after-feedback scenario activity, naming a useful topic to revisit without scoring.
- Keep learned-word expansion with icons, and add a bilingual “Did you know?” card prioritized from terms viewed this week, with two generic fallbacks for new users.
- Preserve the family-sharing controls and localize them.

## 7. Verify
- Check English and Hindi on landing/login, Home, glossary modal/quiz, practice feedback, recap, Assistant, and Account.
- Confirm Devanagari renders without missing-glyph boxes, language changes immediately and survives refresh, OTP focus/countdown/validation work, quiz navigation works, and recap reacts to recorded activity.
- Verify desktop layouts at 1280px and a wider viewport, confirm the narrow-screen guidance remains intentional, and finish with current build/runtime diagnostics clear.

## Technical details
- Keep all routes and the existing `_app` shell structure unchanged.
- Use browser storage only for this mock app’s language and learning activity; no account system or remote data service is added.
- Introduce typed bilingual content helpers and shared `LanguageSwitcher` / learning-feedback primitives under the existing SafeStep component and data conventions.
- Treat the latest seven-scenario list as authoritative; the current QR Refund and ATM Helper cards are replaced by Shop QR Code, Free Computer Help, and Investment Group. Glossary practice links will point to the closest relevant final scenario.
- Use “Meena” for the greeting/profile name to match the requested localized greeting.
