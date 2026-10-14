import tempfile
import unittest
from pathlib import Path
from exporter import export_result, timestamp

class ExportTests(unittest.TestCase):
    def test_timestamp(self):
        self.assertEqual(timestamp(59.9996), '00:01:00,000')
        self.assertEqual(timestamp(3661.125), '01:01:01,125')

    def test_unicode_and_subtitle(self):
        result = {'text': 'Halo, café!', 'segments': [{'start': 0, 'end': 1.25, 'text': ' Halo, café!'}]}
        with tempfile.TemporaryDirectory() as folder:
            export_result(result, folder)
            self.assertEqual((Path(folder)/'transkrip.txt').read_text(encoding='utf-8'), 'Halo, café!\n')
            self.assertEqual((Path(folder)/'subtitle.srt').read_text(encoding='utf-8'), '1\n00:00:00,000 --> 00:00:01,250\nHalo, café!\n')
            self.assertTrue((Path(folder)/'hasil.json').is_file())
