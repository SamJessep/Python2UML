import glob
import os
import shutil
import unittest
from test.support import run_unittest, TESTFN, skip_unless_symlink, can_symlink
from typing import TypeVar, Iterable, List, cast

T = TypeVar('T')


class GlobTests(unittest.TestCase):

    tempdir = ''

    # JLe: work around mypy issue #231
    def norm(self, first: str, *parts: str) -> str:
        return os.path.normpath(os.path.join(self.tempdir, first, *parts))

    def mktemp(self, *parts: str) -> None:
        filename = self.norm(*parts)
        base, file = os.path.split(filename)
        if not os.path.exists(base):
            os.makedirs(base)
        f = open(filename, 'w')
        f.close()

    def setUp(self) -> None:
        self.tempdir = TESTFN+"_dir"
        self.mktemp('a', 'D')
        self.mktemp('aab', 'F')
        self.mktemp('aaa', 'zzzF')
        self.mktemp('ZZZ')
        self.mktemp('a', 'bcd', 'EF')
        self.mktemp('a', 'bcd', 'efg', 'ha')
        if can_symlink():
            os.symlink(self.norm('broken'), self.norm('sym1'))
            os.symlink(self.norm('broken'), self.norm('sym2'))

    def tearDown(self) -> None:
        shutil.rmtree(self.tempdir)

    def glob(self, *parts: str) -> List[str]:
        if len(parts) == 1:
            pattern = parts[0]
        else:
            pattern = os.path.join(*parts)
        p = os.path.join(self.tempdir, pattern)
        res = glob.glob(p)
        self.assertEqual(list(glob.iglob(p)), res)
        return res

    def assertSequencesEqual_noorder(self, l1: Iterable[T],
                                     l2: Iterable[T]) -> None:
        self.assertEqual(set(l1), set(l2))

    def test_glob_literal(self) -> None:
        eq = self.assertSequencesEqual_noorder
        eq(self.glob('a'), [self.norm('a')])
        eq(self.glob('a', 'D'), [self.norm('a', 'D')])
        eq(self.glob('aab'), [self.norm('aab')])
        eq(self.glob('zymurgy'), cast(List[str], []))  # JLe: work around #230

        # test return types are unicode, but only if os.listdir
        # returns unicode filenames
        uniset = set([str])
        tmp = os.listdir('.')
        if set(type(x) for x in tmp) == uniset:
            u1 = glob.glob('*')
            u2 = glob.glob('./*')
            self.assertEqual(set(type(r) for r in u1), uniset)
            self.assertEqual(set(type(r) for r in u2), uniset)

    def test_glob_one_directory(self) -> None:
        eq = self.assertSequencesEqual_noorder
        eq(self.glob('a*'), map(self.norm, ['a', 'aab', 'aaa']))
        eq(self.glob('*a'), map(self.norm, ['a', 'aaa']))
        eq(self.glob('aa?'), map(self.norm, ['aaa', 'aab']))
        eq(self.glob('aa[ab]'), map(self.norm, ['aaa', 'aab']))
        eq(self.glob('*q'), cast(List[str], []))  # JLe: work around #230

    def test_glob_nested_directory(self) -> None:
        eq = self.assertSequencesEqual_noorder
        if os.path.normcase("abCD") == "abCD":
            # case-sensitive filesystem
            eq(self.glob('a', 'bcd', 'E*'), [self.norm('a', 'bcd', 'EF')])
        else:
            # case insensitive filesystem
            eq(self.glob('a', 'bcd', 'E*'), [self.norm('a', 'bcd', 'EF'),
                                             self.norm('a', 'bcd', 'efg')])
        eq(self.glob('a', 'bcd', '*g'), [self.norm('a', 'bcd', 'efg')])

    def test_glob_directory_names(self) -> None:
        eq = self.assertSequencesEqual_noorder
        eq(self.glob('*', 'D'), [self.norm('a', 'D')])
        eq(self.glob('*', '*a'), cast(List[str], []))  # JLe: work around #230
        eq(self.glob('a', '*', '*', '*a'),
           [self.norm('a', 'bcd', 'efg', 'ha')])
        eq(self.glob('?a?', '*F'), map(self.norm, [os.path.join('aaa', 'zzzF'),
                                                   os.path.join('aab', 'F')]))

    def test_glob_directory_with_trailing_slash(self) -> None:
        # We are verifying that when there is wildcard pattern which
        # ends with os.sep doesn't blow up.
        res = glob.glob(self.tempdir + '*' + os.sep)
        self.assertEqual(len(res), 1)
        # either of these results are reasonable
        self.assertIn(res[0], [self.tempdir, self.tempdir + os.sep])

    @skip_unless_symlink
    def test_glob_broken_symlinks(self) -> None:
        eq = self.assertSequencesEqual_noorder
        eq(self.glob('sym*'), [self.norm('sym1'), self.norm('sym2')])
        eq(self.glob('sym1'), [self.norm('sym1')])
        eq(self.glob('sym2'), [self.norm('sym2')])


def test_main() -> None:
    run_unittest(GlobTests)


if __name__ == "__main__":
    test_main()
