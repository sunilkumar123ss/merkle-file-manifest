import importlib.util
from pathlib import Path
import sys
import unittest
_spec = importlib.util.spec_from_file_location('lab_' + Path(__file__).parent.name.replace('-', '_'), Path(__file__).with_name('main.py'))
m = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = m
_spec.loader.exec_module(m)
import tempfile

class MerkleTests(unittest.TestCase):

    def test_nested_paths_follow_manifest_sort_order(self):
        (self.base / 'a').mkdir()
        (self.base / 'a' / 'child').write_text('nested')
        (self.base / 'a.txt').write_text('sibling')
        manifest = m.build(self.base)
        self.assertEqual([row['path'] for row in manifest['entries']], ['a.txt', 'a/child'])
        self.assertTrue(m.compare(manifest, manifest)['matches'])

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()






if __name__ == '__main__':
    unittest.main()
