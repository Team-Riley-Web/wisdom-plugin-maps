#!/usr/bin/env python3
"""Regression checks for pinned downloads and user-mediated author pages."""
import copy
import unittest
import tomllib

import jsonschema
import validate


class CatalogTests(unittest.TestCase):
    def setUp(self):
        self.path = validate.ROOT / "catalog" / "pitchcure.toml"
        self.entry = tomllib.loads(self.path.read_text())

    def problems(self, entry):
        return list(jsonschema.Draft202012Validator(validate.CATALOG_SCHEMA).iter_errors(entry)) or validate.catalog_rules(self.path, entry)

    def test_author_page_is_not_a_download(self):
        self.assertFalse(self.problems(self.entry))
        self.assertEqual(self.entry["downloads"], [])
        self.assertEqual(self.entry["license_kind"], "freeware")
        self.assertEqual({p["platform"] for p in self.entry["pages"]}, {"macos-universal", "windows-x86_64"})

    def test_incomplete_or_ambiguous_pages_are_refused(self):
        for change in [
            lambda e: e.update(pages=[]),
            lambda e: e["pages"][0].update(url="http://example.com"),
            lambda e: e["pages"][0].update(requirements=""),
            lambda e: e["pages"][0].update(sha256="a" * 64),
            lambda e: e["pages"].append(copy.deepcopy(e["pages"][0])),
            lambda e: e["pages"].pop(),
        ]:
            entry = copy.deepcopy(self.entry)
            change(entry)
            self.assertTrue(self.problems(entry))

    def test_downloads_still_require_pins(self):
        path = validate.ROOT / "catalog" / "pitchnet.toml"
        entry = tomllib.loads(path.read_text())
        self.assertFalse(validate.catalog_rules(path, entry))
        for key in ["size", "sha256"]:
            bad = copy.deepcopy(entry)
            del bad["downloads"][0][key]
            self.assertTrue(list(jsonschema.Draft202012Validator(validate.CATALOG_SCHEMA).iter_errors(bad)))


if __name__ == "__main__":
    unittest.main()
