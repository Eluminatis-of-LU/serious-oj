import unittest

from vj4.model import builtin


class GetRatingRankTest(unittest.TestCase):
  def _slug(self, rating):
    rank = builtin.get_rating_rank(rating)
    return rank['slug'] if rank else None

  def test_unrated_returns_none(self):
    self.assertIsNone(builtin.get_rating_rank(None))

  def test_zero_and_negative_are_novice(self):
    self.assertEqual(self._slug(0), 'novice')
    self.assertEqual(self._slug(-50), 'novice')

  def test_tier_boundaries(self):
    cases = [
        (1099, 'novice'),
        (1100, 'apprentice'),
        (1399, 'apprentice'),
        (1400, 'specialist'),
        (1699, 'specialist'),
        (1700, 'expert'),
        (1999, 'expert'),
        (2000, 'master'),
        (2299, 'master'),
        (2300, 'elite'),
        (2599, 'elite'),
        (2600, 'legend'),
    ]
    for rating, expected in cases:
      self.assertEqual(self._slug(rating), expected, msg='rating=%d' % rating)

  def test_very_high_rating_is_legend(self):
    self.assertEqual(self._slug(9999), 'legend')

  def test_returns_name_and_slug(self):
    rank = builtin.get_rating_rank(1750)
    self.assertEqual(rank['slug'], 'expert')
    self.assertEqual(rank['name'], 'Expert')


if __name__ == '__main__':
  unittest.main()
