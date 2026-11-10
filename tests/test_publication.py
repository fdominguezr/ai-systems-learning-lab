import tempfile
import unittest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts.check_publication import check

class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.series = self.root / 'experiments/demo'
        self.series.mkdir(parents=True)
        (self.root/'README.md').write_text('# Index\n[Demo](experiments/demo/README.md)')
        (self.series/'README.md').write_text('# Demo\n[Next](article.md)')
        (self.series/'article.md').write_text('# Article\n[Index](README.md)')

    def test_valid_series(self):
        self.assertEqual(check(self.root), [])

    def test_missing_asset_and_empty_alt(self):
        (self.series/'article.md').write_text('# Article\n[Index](README.md)\n![](missing.png)')
        errors = check(self.root)
        self.assertTrue(any('alt text' in x for x in errors))
        self.assertTrue(any('missing local target' in x for x in errors))

    def test_unindexed_series(self):
        (self.root/'README.md').write_text('# Index')
        self.assertTrue(any('missing from index' in x for x in check(self.root)))

    def test_dead_end_article(self):
        (self.series/'article.md').write_text('# Article')
        self.assertTrue(any('navigation' in x for x in check(self.root)))

    def test_escape_rejected(self):
        (self.series/'article.md').write_text('# Article\n[Index](README.md)\n[X](../../../outside)')
        self.assertTrue(any('escapes repository' in x for x in check(self.root)))

    def test_fragment_not_treated_as_file(self):
        (self.series/'article.md').write_text('# Article\n[Index](README.md#section)')
        self.assertEqual(check(self.root), [])

if __name__ == '__main__':
    unittest.main()
