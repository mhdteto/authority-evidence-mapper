import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

SPEC = importlib.util.spec_from_file_location('mapper', Path(__file__).resolve().parents[1] / 'map_evidence.py')
m = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(m)

class MapperTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.claims = [{'claim_id':'c1','entity':'Example','claim_text':'An example claim'}, {'claim_id':'c2','entity':'Example','claim_text':'Missing'}]
        self.row = dict(evidence_id='e1', claim_id='c1', source_url='https://example.org/a', publisher='Example Press', published_on='2026-01-01', accessed_on='2026-10-01', relationship='independent', support_status='supports', review_note='Reviewed by a human')
    def tearDown(self):
        self.tmp.cleanup()
    def build(self, rows=None, claims=None):
        return m.build_report(self.claims if claims is None else claims, [self.row] if rows is None else rows, '2026-11-01', 180)
    def test_missing_is_not_support(self):
        report = self.build()
        self.assertEqual(report['claims'][1]['statuses'], ['missing evidence'])
        self.assertEqual(report['claims'][1]['independent_support_publishers'], 0)
    def test_distinct_publishers_and_contrary_evidence(self):
        repeated = dict(self.row, evidence_id='e2', publisher=' example   PRESS ')
        contrary = dict(self.row, evidence_id='e3', publisher='Other', support_status='contradicts')
        claim = self.build([self.row,repeated,contrary])['claims'][0]
        self.assertEqual(claim['distinct_publishers'], 2)
        self.assertEqual(claim['independent_support_publishers'], 1)
        self.assertIn('conflicting sources', claim['statuses'])
        self.assertIn('supporting sources', claim['statuses'])
    def test_unknown_and_partial_not_independent_support(self):
        rows = [dict(self.row, relationship='unknown'), dict(self.row,evidence_id='e2',support_status='partial'), dict(self.row,evidence_id='e3',support_status='unreviewed')]
        claim = self.build(rows)['claims'][0]
        self.assertEqual(claim['independent_support_publishers'],0)
        self.assertIn('unreviewed',claim['statuses'])
        self.assertIn('partial',claim['statuses'])
    def test_age_is_review_age(self):
        rows = [dict(self.row,accessed_on='2026-01-01'),dict(self.row,evidence_id='e2',accessed_on='')]
        evidence = self.build(rows)['claims'][0]['evidence']
        self.assertEqual(evidence[0]['review_age'],'stale')
        self.assertEqual(evidence[1]['review_age'],'unknown')
        self.assertEqual(self.build(rows)['claims'][0]['independent_support_publishers'],1)
    def test_stale_threshold(self):
        report=m.build_report(self.claims,[self.row],'2026-11-01',30)
        self.assertEqual(report['claims'][0]['evidence'][0]['review_age'],'stale')
    def test_dates_rejected(self):
        for changes in [{'accessed_on':'bad'},{'published_on':'2026-02-30'},{'accessed_on':'2026-12-01'},{'published_on':'2026-12-01'},{'published_on':'2026-10-02'}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.build([dict(self.row,**changes)])
    def test_duplicates_and_reference_rejected(self):
        for rows in [[self.row,self.row],[dict(self.row,claim_id='absent')]]:
            with self.assertRaises(ValueError): self.build(rows)
        with self.assertRaises(ValueError): self.build(claims=[self.claims[0],self.claims[0]])
    def test_bad_fields_rejected(self):
        for changes in [{'publisher':'  '},{'evidence_id':''},{'relationship':'trusted'},{'support_status':'verified'},{'source_url':'javascript:alert(1)'},{'source_url':'file:///etc/passwd'}]:
            with self.subTest(changes=changes), self.assertRaises(ValueError): self.build([dict(self.row,**changes)])
    def test_html_and_csv_safe(self):
        report=self.build([dict(self.row,review_note='<script>alert(1)</script>',publisher='=1+1')], [dict(self.claims[0],claim_text='<img src=x onerror=alert(1)>')])
        m.write_reports(report,self.root)
        html=(self.root/'report.html').read_text()
        self.assertNotIn('<script>',html)
        self.assertIn('&lt;script&gt;',html)
        self.assertNotIn('<img src=x',html)
        with (self.root/'evidence.csv').open(newline='') as f: rows=list(csv.DictReader(f))
        self.assertEqual(rows[0]['publisher'],"'=1+1")
    def test_csv_headers_and_extra_cells_rejected(self):
        p=self.root/'bad.csv'; p.write_text('claim_id,entity\nc1,Example\n')
        with self.assertRaises(ValueError): m.read_csv(p,m.CLAIM_FIELDS)
        p.write_text('claim_id,entity,claim_text\nc1,Example,Text,extra\n')
        with self.assertRaises(ValueError): m.read_csv(p,m.CLAIM_FIELDS)
    def test_required_claim_fields(self):
        for field in m.CLAIM_FIELDS:
            with self.subTest(field=field), self.assertRaises(ValueError):
                self.build(claims=[dict(self.claims[0], **{field: ' '})])
    def test_safe_url_attribute_and_formula_variants(self):
        report=self.build([dict(self.row,source_url='https://example.org/?q="onmouseover="alert(1)')])
        html=m.html_report(report)
        self.assertIn('&quot;onmouseover=&quot;',html)
        self.assertNotIn('q="onmouseover=',html)
        for value in ['=SUM(A1:A2)', '+1', '-1', '@SUM(A1)', '  =1', '\t=1']:
            self.assertTrue(m.csv_safe(value).startswith("'"))
    def test_output_collision_preserves_inputs(self):
        claims=self.root/'claims.csv'
        evidence=self.root/'evidence.csv'
        claims.write_text('claim_id,entity,claim_text\nc1,Example,Claim\n')
        evidence.write_text(','.join(m.EVIDENCE_FIELDS)+'\n')
        before=(claims.read_bytes(),evidence.read_bytes())
        with self.assertRaises(SystemExit) as raised:
            m.main(['--claims',str(claims),'--evidence',str(evidence),'--as-of','2026-11-01','--output-dir',str(self.root)])
        self.assertEqual(raised.exception.code,2)
        self.assertEqual((claims.read_bytes(),evidence.read_bytes()),before)
        self.assertFalse((self.root/'report.json').exists())
    def test_output_collision_resolves_symlinks(self):
        source=self.root/'original.csv'
        source.write_text('claim_id,entity,claim_text\nc1,Example,Claim\n')
        evidence=self.root/'input-evidence.csv'
        evidence.write_text(','.join(m.EVIDENCE_FIELDS)+'\n')
        output=self.root/'output'
        output.mkdir()
        (output/'report.html').symlink_to(source)
        with self.assertRaises(SystemExit) as raised:
            m.main(['--claims',str(source),'--evidence',str(evidence),'--as-of','2026-11-01','--output-dir',str(output)])
        self.assertEqual(raised.exception.code,2)
        self.assertTrue(source.read_text().startswith('claim_id,'))
        self.assertFalse((output/'report.json').exists())
    def test_malformed_quoted_csv_rejected_before_reports(self):
        claims=self.root/'input-claims.csv'
        evidence=self.root/'input-evidence.csv'
        output=self.root/'reports'
        claims.write_text('claim_id,entity,claim_text\nc1,Example,Claim\n')
        evidence.write_text(','.join(m.EVIDENCE_FIELDS)+'\ne1,c1,https://example.org/a,Example,2026-01-01,2026-10-01,independent,supports,"unterminated\n')
        with self.assertRaises(SystemExit) as raised:
            m.main(['--claims',str(claims),'--evidence',str(evidence),'--as-of','2026-11-01','--output-dir',str(output)])
        self.assertEqual(raised.exception.code,2)
        self.assertFalse(output.exists())
    def test_invalid_configuration(self):
        for date,days in [('invalid',180),('2026-11-01',-1)]:
            with self.assertRaises(ValueError): m.build_report(self.claims,[],date,days)

if __name__=='__main__': unittest.main()
