import unittest
from compact_roles import compact_prompt,GUIDANCE
class CompactRoleTests(unittest.TestCase):
    def test_every_nondecision_role_preserves_prompt(self):
        original='Original task and prior drafts; no external actions or fabricated evidence.'
        self.assertEqual(set(GUIDANCE),{'assign','build_act','dissent','revision','outcome'})
        for role in GUIDANCE:
            with self.subTest(role=role):
                result=compact_prompt(role,original)
                self.assertTrue(result.startswith(original))
                self.assertIn('All original requirements and safety rules remain binding',result)
                self.assertIn('do not omit material limitations',result)
    def test_decision_roles_not_overridden(self):
        for role in ('scout','verify','safety','unknown'):
            with self.assertRaises(ValueError):compact_prompt(role,'original')
    def test_prompt_length_and_input_guard(self):
        for value in ('','x'*12000,None):
            with self.assertRaises(ValueError):compact_prompt('assign',value)
    def test_assign_keeps_provenance_and_review(self):
        result=compact_prompt('assign','Original')
        for term in ('primary-source/date/hash','separate human review','Do not add authorization'):
            self.assertIn(term,result)
