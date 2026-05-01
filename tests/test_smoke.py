"""Smoke tests for ml-automation-mmm — validate plugin layout invariants."""

import json
import re
from pathlib import Path

import pytest


PLUGIN_ROOT = Path(__file__).resolve().parent.parent


class TestManifestValidity:
    """Validate plugin manifest structure and required fields."""

    def test_manifest_file_exists(self):
        """Manifest file exists and is readable."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        assert manifest_path.exists(), "Manifest file .cortex-plugin/plugin.json not found"
        assert manifest_path.is_file(), "Manifest path is not a file"

    def test_manifest_valid_json(self):
        """Manifest is valid JSON."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        try:
            with open(manifest_path, "r") as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Manifest is not valid JSON: {e}")

    def test_manifest_required_fields(self):
        """Manifest contains all required fields."""
        manifest_path = PLUGIN_ROOT / ".cortex-plugin" / "plugin.json"
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        required_fields = ["name", "version", "description", "cortex"]
        for field in required_fields:
            assert field in manifest, f"Missing required field: {field}"

        assert "agents_dir" in manifest["cortex"], "Missing cortex.agents_dir"
        assert "skills_dir" in manifest["cortex"], "Missing cortex.skills_dir"


class TestAgentsSkillsReferentialIntegrity:
    """Validate AGENTS.md ↔ agents/ and skills/ directory alignment."""

    def test_agents_md_exists(self):
        """AGENTS.md file exists."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        assert agents_md.exists(), "AGENTS.md not found"

    def test_agents_referenced_in_md_exist_as_files(self):
        """Every agent listed in AGENTS.md has a corresponding agents/<name>.md file."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        agents_dir = PLUGIN_ROOT / "agents"

        with open(agents_md, "r") as f:
            content = f.read()

        agent_pattern = r"^\|\s*`([a-z-]+)`\s*\|"
        agents_found = set()

        in_agents_section = False
        for line in content.split("\n"):
            if "## Available Agents" in line:
                in_agents_section = True
                continue
            if in_agents_section and line.startswith("## "):
                in_agents_section = False
            if in_agents_section:
                match = re.match(agent_pattern, line)
                if match:
                    agents_found.add(match.group(1))

        agent_files = {f.stem for f in agents_dir.glob("*.md")}

        missing_files = agents_found - agent_files
        assert not missing_files, f"Agents in AGENTS.md lack corresponding files: {missing_files}"

    def test_skills_referenced_in_md_exist_as_directories(self):
        """Every skill listed in AGENTS.md has a corresponding skills/<name>/ directory."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        skills_dir = PLUGIN_ROOT / "skills"

        with open(agents_md, "r") as f:
            content = f.read()

        skill_pattern = r"^\|\s*`/([a-z-]+)`\s*\|"
        skills_found = set()

        in_skills_section = False
        for line in content.split("\n"):
            if "## Available Skills" in line:
                in_skills_section = True
                continue
            if in_skills_section and line.startswith("## "):
                in_skills_section = False
            if in_skills_section:
                match = re.match(skill_pattern, line)
                if match:
                    skills_found.add(match.group(1))

        skill_dirs = {d.name for d in skills_dir.iterdir() if d.is_dir()}

        missing_dirs = skills_found - skill_dirs
        assert not missing_dirs, f"Skills in AGENTS.md lack corresponding directories: {missing_dirs}"

    def test_skill_directories_contain_skill_md(self):
        """Every skill directory contains a SKILL.md file."""
        skills_dir = PLUGIN_ROOT / "skills"

        for skill_dir in skills_dir.iterdir():
            if skill_dir.is_dir():
                skill_md = skill_dir / "SKILL.md"
                assert skill_md.exists(), f"Skill {skill_dir.name} missing SKILL.md"

    def test_agent_files_are_referenced_in_agents_md(self):
        """Every agents/<name>.md file has a corresponding entry in AGENTS.md."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        agents_dir = PLUGIN_ROOT / "agents"

        with open(agents_md, "r") as f:
            content = f.read()

        agent_pattern = r"^\|\s*`([a-z-]+)`\s*\|"
        agents_referenced = set()

        in_agents_section = False
        for line in content.split("\n"):
            if "## Available Agents" in line:
                in_agents_section = True
                continue
            if in_agents_section and line.startswith("## "):
                in_agents_section = False
            if in_agents_section:
                match = re.match(agent_pattern, line)
                if match:
                    agents_referenced.add(match.group(1))

        agent_files = {f.stem for f in agents_dir.glob("*.md")}

        orphaned_agents = agent_files - agents_referenced
        assert not orphaned_agents, f"Orphaned agent files not in AGENTS.md: {orphaned_agents}"

    def test_skill_directories_are_referenced_in_agents_md(self):
        """Every skills/<name>/ directory has a corresponding entry in AGENTS.md."""
        agents_md = PLUGIN_ROOT / "AGENTS.md"
        skills_dir = PLUGIN_ROOT / "skills"

        with open(agents_md, "r") as f:
            content = f.read()

        skill_pattern = r"^\|\s*`/([a-z-]+)`\s*\|"
        skills_referenced = set()

        in_skills_section = False
        for line in content.split("\n"):
            if "## Available Skills" in line:
                in_skills_section = True
                continue
            if in_skills_section and line.startswith("## "):
                in_skills_section = False
            if in_skills_section:
                match = re.match(skill_pattern, line)
                if match:
                    skills_referenced.add(match.group(1))

        skill_dirs = {d.name for d in skills_dir.iterdir() if d.is_dir()}

        orphaned_skills = skill_dirs - skills_referenced
        assert not orphaned_skills, f"Orphaned skill directories not in AGENTS.md: {orphaned_skills}"
