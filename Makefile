# OpenSpec project — convenience targets.
# Wraps the most common workflow commands so contributors don't have to
# remember script paths. All targets are thin shims over scripts/openspec
# and project tooling — no logic lives here.

SHELL := /usr/bin/env bash
.SHELLFLAGS := -eu -o pipefail -c
.DEFAULT_GOAL := help

OPENSPEC := scripts/openspec

# Read testing.test_command from .openspec/config.yaml (best-effort).
TEST_CMD := $(shell grep -E '^[[:space:]]*test_command:' .openspec/config.yaml 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*test_command:[[:space:]]*//' | sed -E 's/^"(.*)"$$/\1/')

.PHONY: help setup check check-strict scaffold scaffold-bug test scenario-schema validate arxiv-check reproducibility-report release-check status clean cleanup-template-specs apply-branch-protection

help:  ## Show this help
	@awk '/^[a-zA-Z_-]+:.*## / { split($$0, target, ":"); description = $$0; sub(/^[^#]*## /, "", description); printf "  \033[36m%-16s\033[0m %s\n", target[1], description }' $(MAKEFILE_LIST)

setup:  ## Install git hooks and make scripts/openspec executable
	bash setup.sh

check:  ## Validate every spec in .openspec/specs/
	$(OPENSPEC) check

check-strict:  ## Validate specs and treat 'draft' status as failure
	$(OPENSPEC) check --strict

scaffold:  ## Create a new feature spec.  Usage: make scaffold name="my feature"
	@if [ -z "$(name)" ]; then echo 'usage: make scaffold name="my feature"'; exit 2; fi
	$(OPENSPEC) scaffold "$(name)"

scaffold-bug:  ## Create a new bugfix spec.  Usage: make scaffold-bug name="login crash"
	@if [ -z "$(name)" ]; then echo 'usage: make scaffold-bug name="login crash"'; exit 2; fi
	$(OPENSPEC) scaffold "$(name)" --type bugfix

test:  ## Run testing.test_command from .openspec/config.yaml
	@if [ -z "$(TEST_CMD)" ] || echo "$(TEST_CMD)" | grep -q '{{'; then \
		echo "error: testing.test_command not configured in .openspec/config.yaml"; exit 1; \
	fi
	@echo "→ $(TEST_CMD)"
	@bash -c '$(TEST_CMD)'

scenario-schema:  ## Validate all scenario manifests against spec/schema.yaml
	python3 -m pytest tests/test_schema.py

validate: check test scenario-schema  ## Run all deterministic repository validation

arxiv-check:  ## Compile the extracted arXiv source archive and check its log
	bash paper/v3/check-arxiv.sh

reproducibility-report:  ## Write read-only provenance and evidence hashes to out/
	python3 scripts/reproducibility_report.py --output out/reproducibility-report.json

release-check: validate arxiv-check  ## Validate repository, arXiv package, and provenance
	python3 scripts/reproducibility_report.py --output out/reproducibility-report.json \
		--check openspec=passed --check pytest=passed --check scenario_schema=passed

status:  ## Show OpenSpec configuration status
	@if grep -q '{{' .openspec/config.yaml 2>/dev/null; then \
		echo "STATUS: NOT_CONFIGURED — run onboarding (open in Claude Code or edit .openspec/config.yaml)"; \
	else \
		echo "STATUS: CONFIGURED"; \
	fi
	@$(OPENSPEC) check 2>&1 | tail -5 || true

clean:  ## Remove generated artifacts (sandbox/test specs only — never touches .openspec/specs/)
	@find . -name '*.bak' -not -path './.git/*' -delete
	@echo "✓ removed .bak files"

cleanup-template-specs:  ## Remove the template's internal design specs (run once on a fresh fork)
	bash scripts/cleanup-template-specs

apply-branch-protection:  ## Push the default-branch ruleset to GitHub (requires gh CLI + admin)
	bash scripts/apply-branch-protection
