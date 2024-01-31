# GitHub Actions for Dewy

We currently have the following workflows:

1. `ci.yml` defines the CI process for the core service and clients.
2. `lint-pr.yml`: Checks PRs for style, naming, and provides some automation.
  - Verifies the title of the PR conforms to conventional commits.
  - Runs an "autolabeler" to provide labels based on title and files touched.
3. `site.yml` defines the build and deployment process for the site.
4. `release-drafter.yml`: Generates draft release notes as PRs are merged.
5. `sync-labels.yml`: Updates the labels in the project to match `.github/labels.yml`.

## Future Improvements

- Require conditional checks https://github.com/marketplace/actions/require-conditional-status-checks