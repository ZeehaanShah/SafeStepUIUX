<!-- LOVABLE:BEGIN -->
> [!IMPORTANT]
> This project is connected to [Lovable](https://lovable.dev). Avoid rewriting
> published git history — force pushing, or rebasing/amending/squashing commits
> that are already pushed — as it rewrites history on Lovable's side and the
> user will likely lose their project history.
>
> Commits you push to the connected branch sync back to Lovable and show up in
> the editor, so keep the branch in a working state.
<!-- LOVABLE:END -->

## Project structure
- App screens live under the `_app` layout route (sidebar shell in `src/components/safestep/app-shell.tsx`); `/` and `/login` stay outside it because they are pre-login screens.
- Shared SafeStep UI primitives live in `src/components/safestep/ui.tsx` and mock content in `src/lib/safestep-data.ts`, so no screen defines one-off styled variants.
