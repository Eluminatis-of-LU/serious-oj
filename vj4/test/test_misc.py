import unittest

from vj4.util import misc


class Test(unittest.TestCase):
  def test_dedupe(self):
    self.assertListEqual(misc.dedupe([2,1,1,3,2,3]),[2,1,3])
    self.assertListEqual(misc.dedupe([]),[])
    self.assertListEqual(misc.dedupe(map(int,['2','1','1','3','2','3'])),[2,1,3])
    self.assertListEqual(misc.dedupe(['b','a','b','c','b']),['b','a','c'])
    self.assertListEqual(misc.dedupe([0]),[0])


class ProblemLabelTest(unittest.TestCase):
  def test_first_letters(self):
    self.assertEqual(misc.problem_label(0), 'A')
    self.assertEqual(misc.problem_label(1), 'B')
    self.assertEqual(misc.problem_label(25), 'Z')

  def test_double_letters(self):
    self.assertEqual(misc.problem_label(26), 'AA')
    self.assertEqual(misc.problem_label(27), 'AB')
    self.assertEqual(misc.problem_label(51), 'AZ')
    self.assertEqual(misc.problem_label(52), 'BA')

  def test_rejects_negative(self):
    with self.assertRaises(ValueError):
      misc.problem_label(-1)


if __name__ == '__main__':
  unittest.main()
