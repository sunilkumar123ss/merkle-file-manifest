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

    def test_empty_is_stable(self):
        self.assertEqual(m.build(self.base), m.build(self.base))

    def test_changes_are_localized(self):
        (self.base / 'a').write_text('one')
        before = m.build(self.base)
        (self.base / 'a').write_text('two')
        result = m.compare(before, m.build(self.base))
        self.assertFalse(result['matches'])
        self.assertEqual(result['changed'], ['a'])

    def test_added_and_removed(self):
        (self.base / 'a').write_text('one')
        before = m.build(self.base)
        (self.base / 'a').unlink()
        (self.base / 'b').write_text('two')
        result = m.compare(before, m.build(self.base))
        self.assertEqual(result['added'], ['b'])
        self.assertEqual(result['removed'], ['a'])

    def test_creation_order_does_not_matter(self):
        for name in ['c', 'a', 'b']:
            (self.base / name).write_text(name)
        first = m.build(self.base)
        for file in self.base.iterdir():
            file.unlink()
        for name in ['a', 'b', 'c']:
            (self.base / name).write_text(name)
        self.assertEqual(first, m.build(self.base))

    def test_symlinks_rejected(self):
        (self.base / 'a').write_text('x')
        (self.base / 'link').symlink_to(self.base / 'a')
        with self.assertRaises(ValueError):
            m.build(self.base)

if __name__ == '__main__':
    unittest.main()
