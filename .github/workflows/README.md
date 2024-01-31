# GitHub Actions for Dewy

We currently have 3 workflows:

1. `ci.yml` defines the CI process for the core service and clients.
2. `lint-pr.yml` defines linting of the PR itself (comments, etc.).
3. `site.yml` defines the build and deployment process for the site.

## Future Improvements

1. Release drafting / publishing.
2. Assign labels to PRs based on directories touched (eg., `docs`, `service`, etc.) and
   conventional commit (`fix`, `feature`, etc.).
3. Require conditional checks https://github.com/marketplace/actions/require-conditional-status-checks