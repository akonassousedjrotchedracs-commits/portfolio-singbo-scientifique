import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if "id" in attributes:
            self.ids.add(attributes["id"])
        for key in ("href", "src"):
            if attributes.get(key):
                self.links.append(attributes[key])


class PortfolioAuditTests(unittest.TestCase):
    def test_project_01_fixture_is_ten_pairs_of_ten(self):
        path = ROOT / "project_01_antimicrobial_resistance/results/amr_observations_synthetic_100.csv"
        with path.open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        pairs = {(row["organism"], row["antibiotic"]) for row in rows}
        self.assertEqual(len(rows), 100)
        self.assertEqual(len(pairs), 10)
        self.assertEqual({pair: sum((row["organism"], row["antibiotic"]) == pair for row in rows) for pair in pairs}, {pair: 10 for pair in pairs})
        self.assertTrue({row["result"] for row in rows} <= {"S", "I", "R"})

    def test_project_02_fasta_rejects_non_iupac_and_accepts_ambiguity(self):
        module = load_module("fasta_qc", ROOT / "project_02_bacterial_sequence/scripts/reproduce.py")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "sequence.fasta"
            path.write_text(">valid\nACGTNRY\n", encoding="ascii")
            self.assertEqual(module.read_fasta(path)[0][1], "ACGTNRY")
            path.write_text(">invalid\nACGTZ\n", encoding="ascii")
            with self.assertRaises(ValueError):
                module.read_fasta(path)
            path.write_text(">empty\n", encoding="ascii")
            with self.assertRaises(ValueError):
                module.read_fasta(path)
            path.write_text(">duplicate\nACGT\n>duplicate\nTGCA\n", encoding="ascii")
            with self.assertRaises(ValueError):
                module.read_fasta(path)

    def test_project_02_fastq_rejects_invalid_records(self):
        module = load_module("fastq_qc", ROOT / "project_02_bacterial_sequence/scripts/reproduce_fastq_qc.py")
        with tempfile.TemporaryDirectory() as temporary:
            path = Path(temporary) / "reads.fastq"
            path.write_text("@read1\nACGTN\n+\n!!!!!\n", encoding="ascii")
            self.assertEqual(len(module.parse(path)), 1)
            for content in (
                "@read1\nACGT\n+\n!!!\n",
                "@read1\nACGZ\n+\n!!!!\n",
                "@read1\nACGT\n+other\n!!!!\n",
                "@read1\n\n+\n\n",
                "@read1\nACGT\n+\n!!!\nextra\n",
            ):
                path.write_text(content, encoding="ascii")
                with self.assertRaises(ValueError):
                    module.parse(path)

    def test_project_03_pipeline_preserves_invalid_rows_in_audit(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "results"
            subprocess.run([
                sys.executable,
                str(ROOT / "project_03_sql_advanced/scripts/run_pipeline.py"),
                "--input", str(ROOT / "project_03_sql_advanced/data/TEST_FIXTURE_with_anomalies.csv"),
                "--output-dir", str(output),
            ], cwd=ROOT, check=True, capture_output=True, text=True)
            with (output / "data_quality_issues.csv").open(newline="", encoding="utf-8") as handle:
                issues = list(csv.DictReader(handle))
            manifest = json.loads((output / "provenance_manifest.json").read_text(encoding="utf-8"))
            self.assertEqual([issue["issue"] for issue in issues].count("missing_required_value"), 1)
            self.assertEqual([issue["issue"] for issue in issues].count("invalid_result"), 1)
            self.assertEqual([issue["issue"] for issue in issues].count("duplicate_isolate_antibiotic"), 1)
            self.assertEqual(manifest["rows_received"], 5)
            self.assertEqual(manifest["rows_curated"], 2)

    def test_project_04_wilson_uses_counts_and_valid_denominator(self):
        module = load_module("wilson", ROOT / "project_04_advanced_biomedical_analysis/scripts/reproduce.py")
        lower, upper = module.wilson(16, 50)
        self.assertAlmostEqual(lower * 100, 20.7580441, places=5)
        self.assertAlmostEqual(upper * 100, 45.8105571, places=5)
        with (ROOT / "project_04_advanced_biomedical_analysis/data/DEMO_SYNTHETIC_wilson.csv").open(newline="", encoding="utf-8-sig") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 300)
        self.assertEqual({row["result"] for row in rows}, {"S", "I", "R"})
        keys = [(row["isolate_id"], row["antibiotic"]) for row in rows]
        self.assertEqual(len(keys), len(set(keys)))

    def test_internal_html_links_and_images_resolve(self):
        failures = []
        for page in ROOT.rglob("*.html"):
            parser = LinkCollector()
            parser.feed(page.read_text(encoding="utf-8"))
            for link in parser.links:
                if link.startswith(("http:", "https:", "mailto:", "tel:", "data:", "javascript:")):
                    continue
                target, _, fragment = link.partition("#")
                destination = (page.parent / target).resolve() if target else page.resolve()
                if not destination.exists():
                    failures.append(f"{page.relative_to(ROOT)} -> {link}")
                elif fragment and destination.suffix.lower() == ".html":
                    target_parser = LinkCollector()
                    target_parser.feed(destination.read_text(encoding="utf-8"))
                    if fragment not in target_parser.ids:
                        failures.append(f"{page.relative_to(ROOT)} -> missing #{fragment} in {destination.relative_to(ROOT)}")
        for page in ROOT.rglob("*.md"):
            for link in re.findall(r"\]\(([^)]+)\)", page.read_text(encoding="utf-8")):
                if link.startswith(("http:", "https:", "mailto:", "tel:", "#")):
                    continue
                destination = (page.parent / link.partition("#")[0]).resolve()
                if not destination.exists():
                    failures.append(f"{page.relative_to(ROOT)} -> {link}")
        self.assertEqual(failures, [])


if __name__ == "__main__":
    unittest.main()
