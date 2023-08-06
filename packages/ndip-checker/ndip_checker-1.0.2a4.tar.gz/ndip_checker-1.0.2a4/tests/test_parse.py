"""Test cases for argparse."""
import pytest
import unittest

from ndip_checker.parser_utils import get_parser, parse_args


class ParserTest(unittest.TestCase):
    """Test case for `get_parser`"""

    def setUp(self):
        self.parser = get_parser()

    def test_no_argument(self):
        """test no argument was"""

        args = ''.split()
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args(args)

        assert e.type == SystemExit
        assert e.value.code == 2

    def test_check_all_parameter(self):
        """test all parameter"""

        args = 'all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        with pytest.raises(AttributeError) as e:
            self.assertEqual(parsed.fix, False)

    def test_args_not_match(self):
        """test argument not in the same group"""

        args = 'all -f'.split()
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

    def test_check_dynamic_parameter(self):
        """test check dynamic"""

        args = 'dynamic-treat'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, False)

        args = 'dynamic-treat -f'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, True)

        args = 'dynamic-treat --fix'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, True)

    def test_optional_parameter(self):
        """test optional parameters.
        
        -h/--host
        -u/--user
        -p/--password
        -d/--database
        """
        args = '-o 127.0.0.1 all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, '127.0.0.1')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--host 127.0.0.1 all '.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, '127.0.0.1')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-u yarving all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'yarving')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--user yarving all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'yarving')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-p asdfjkl all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'asdfjkl')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--password asdfjkl all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'asdfjkl')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-d hello all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hello')

        args = '--database hello all'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hello')

    def test_change_enter_date_parameter(self):
        """change enter date parameter"""

        args = 'change-enter-date'.split()
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1'.split()
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1 2018-03-14'.split()
        with pytest.raises(SystemExit) as e:
            self.parser.parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1 2018-03-14 2018-04-14'.split()
        parsed = self.parser.parse_args(args)
        self.assertEqual(parsed.record_id, 1)
        self.assertEqual(parsed.original, '2018-03-14')
        self.assertEqual(parsed.target, '2018-04-14')

        args = 'change-enter-date 1 20180314 2018-04-14'.split()
        with pytest.raises(SystemExit):
            self.parser.parse_args(args)

        args = 'change-enter-date 1 2018-03-14 20180414'.split()
        with pytest.raises(SystemExit):
            self.parser.parse_args(args)


class ParseArgsTest(unittest.TestCase):
    """test case for function `parse_args`"""

    def test_no_argument(self):
        """test no argument was"""

        args = ''.split()
        with pytest.raises(SystemExit) as e:
            parse_args(args)

        assert e.type == SystemExit
        assert e.value.code == 2

    def test_check_all_parameter(self):
        """test all parameter"""

        args = 'all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        with pytest.raises(AttributeError) as e:
            self.assertEqual(parsed.fix, False)

    def test_args_not_match(self):
        """test argument not in the same group"""

        args = 'all -f'.split()
        with pytest.raises(SystemExit) as e:
            parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

    def test_check_dynamic_parameter(self):
        """test check dynamic"""

        args = 'dynamic-treat'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, False)

        args = 'dynamic-treat -f'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, True)

        args = 'dynamic-treat --fix'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')
        self.assertEqual(parsed.fix, True)

    def test_optional_parameter(self):
        """test optional parameters.
        
        -h/--host
        -u/--user
        -p/--password
        -d/--database
        """
        args = '-o 127.0.0.1 all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, '127.0.0.1')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--host 127.0.0.1 all '.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, '127.0.0.1')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-u yarving all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'yarving')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--user yarving all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'yarving')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-p asdfjkl all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'asdfjkl')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '--password asdfjkl all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'asdfjkl')
        self.assertEqual(parsed.database, 'hospitalAdmin')

        args = '-d hello all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hello')

        args = '--database hello all'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.host, 'localhost')
        self.assertEqual(parsed.user, 'root')
        self.assertEqual(parsed.password, 'ChangeMe1!')
        self.assertEqual(parsed.database, 'hello')

    def test_change_enter_date_parameter(self):
        """change enter date parameter"""

        args = 'change-enter-date'.split()
        with pytest.raises(SystemExit) as e:
            parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1'.split()
        with pytest.raises(SystemExit) as e:
            parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1 2018-03-14'.split()
        with pytest.raises(SystemExit) as e:
            parse_args(args)
        assert e.type == SystemExit
        assert e.value.code == 2

        args = 'change-enter-date 1 2018-03-14 2018-04-14'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.record_id, 1)
        self.assertEqual(parsed.original, '2018-03-14')
        self.assertEqual(parsed.target, '2018-04-14')

        args = 'change-enter-date 1 2018-3-14 2018-4-14'.split()
        parsed = parse_args(args)
        self.assertEqual(parsed.record_id, 1)
        self.assertEqual(parsed.original, '2018-03-14')
        self.assertEqual(parsed.target, '2018-04-14')
