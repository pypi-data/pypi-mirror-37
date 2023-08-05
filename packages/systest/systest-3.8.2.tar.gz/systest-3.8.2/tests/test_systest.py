import unittest
import json

import systest
from systest import Sequencer

from tests.testcases.named import NamedTest
from tests.testcases.fail import FailTest
from tests.testcases.fail import FailSetupTest
from tests.testcases.fail import FailTearDownTest
from tests.testcases.fail import FailAssertRaisesNoExceptionTest
from tests.testcases.fail import FailAssertRaisesWrongExceptionTest
from tests.testcases.fail import FailAssertIsNoneTest
from tests.testcases.notexecuted import NotExecutedTest
from tests.testcases.description import DescriptionNoneTest
from tests.testcases.description import DescriptionEmptyTest
from tests.testcases.description import DescriptionBlankTest
from tests.testcases.description import DescriptionMultiLineTest


class SysTestTest(unittest.TestCase):

    def setUp(self):
        NamedTest.count = 0
        NotExecutedTest.count = 0
        FailTest.count = 0

    def test_serial_parallel(self):
        """Run a sequence of serial and parallel tests.

        """

        sequencer = Sequencer("serial_parallel")

        # Run a bunch of tests.
        passed, failed, skipped = sequencer.run(
            NamedTest("a"),
            [
                NamedTest("b")
            ],
            # Tests in a tuple are executed in parallel.
            (
                NamedTest("c", work_time=0.2),
                NamedTest("d"),
                NamedTest("e"),
                (
                    NamedTest("f"),
                    NamedTest("g")
                ),
                NamedTest("h"),
                (
                    NamedTest("i", work_time=0.1),
                    NamedTest("j"),
                    FailTest("a")
                ),
                [
                    FailTest("b"),
                    [
                        NotExecutedTest("a")
                    ]
                ],
                FailTest("c")
            ),
            [
                NotExecutedTest("b")
            ],
            NamedTest("k"),
            NamedTest("l")
        )

        sequencer.report()

        self.assertEqual(passed, 12)
        self.assertEqual(failed, 3)
        self.assertEqual(skipped, 2)
        self.assertEqual(NamedTest.count, 12)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 3)

        json_report = sequencer.summary_json()
        print(json.dumps(json_report, indent=4))
        self.assertEqual(json_report["name"], "serial_parallel")
        self.assertEqual(len(json_report["testcases"]), 17)

    def test_serial_parallel_stop_on_failure(self):
        """Run a sequence of serial and parallel tests and stop on failure.

        """

        sequencer = Sequencer("serial_parallel_stop_on_failure")

        # Run a bunch of tests.
        passed, failed, skipped = sequencer.run(
            NamedTest("a"),
            [
                NamedTest("b")
            ],
            # Tests in a tuple are executed in parallel.
            (
                NamedTest("c", work_time=0.2),
                NamedTest("d"),
                NamedTest("e"),
                (
                    NamedTest("f"),
                    NamedTest("g")
                ),
                NamedTest("h"),
                (
                    NamedTest("i", work_time=0.1),
                    NamedTest("j"),
                    FailTest("a")
                ),
                [
                    FailTest("b"),
                    [
                        NotExecutedTest("a")
                    ]
                ],
                FailTest("c")
            ),
            [
                NotExecutedTest("b")
            ],
            NamedTest("k"),
            NamedTest("l"),
            continue_on_failure=False
        )

        sequencer.report()

        self.assertTrue(passed >= 2)
        self.assertTrue(failed >= 1)
        self.assertTrue(skipped >= 1)
        self.assertEqual(passed + failed + skipped, 17)
        self.assertTrue(NamedTest.count >= 2)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertTrue(FailTest.count >= 1)

    def test_continue_on_failure(self):
        """Run all tests even if a test fails.

        """

        sequencer = Sequencer("continue_on_failure")

        result = sequencer.run(
            FailTest("1"),
            NamedTest("a"),
            (
                FailTest("2"),
                NamedTest("b")
            )
        )

        sequencer.report()

        self.assertEqual(result, (2, 2, 0))
        self.assertEqual(NamedTest.count, 2)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 2)

    def test_dot_digraph(self):
        """Create a dot digraph of given sequence.

        """

        sequencer = Sequencer("dot_digraph",
                              dry_run=True)

        result = sequencer.run(
            NamedTest("a"),
            NamedTest("b"),
            (
                NamedTest("c", work_time=0.2),
                [
                    NamedTest("d"),
                    NamedTest("e"),
                    (
                        NamedTest("f", work_time=1.4),
                        NamedTest("g")
                    ),
                    NamedTest("h"),
                    (
                        NamedTest("i", work_time=0.1),
                        NamedTest("j", work_time=3.2),
                        FailTest("a")
                    ),
                    NotExecutedTest("a")
                ],
                FailTest("b"),
                FailTest("c")
            ),
            NotExecutedTest("b"),
            NamedTest("k"),
            NamedTest("l")
        )

        sequencer.report()

        self.assertEqual(result, (17, 0, 0))

    def test_testcase_filter(self):
        """Use the test execution filter to run a specific testcase in a
        sequence.

        """

        # A testcase in `testcase_skip_filter` will be skipped even if it is
        # in `testcase_filter`.
        sequencer = Sequencer("filter",
                              testcase_filter=["fail_1", "test_b", "test_d"],
                              testcase_skip_filter=["fail_1"])

        result = sequencer.run(
            FailTest("1"),
            NamedTest("a"),
            (
                FailTest("2"),
                NamedTest("b")
            ),
            NamedTest("c"),
            [
                NamedTest("d")
            ]
        )

        sequencer.report()

        self.assertEqual(result, (2, 0, 4))
        self.assertEqual(NamedTest.count, 2)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 0)

    def test_force_serial_execution(self):
        """Force serial test case execution.

        """

        sequencer = Sequencer("forced_serial_execution",
                              force_serial_execution=True)

        result = sequencer.run((
            FailTest("1"),
            NamedTest("a")
        ))

        sequencer.report()

        self.assertEqual(result, (1, 1, 0))
        self.assertEqual(NamedTest.count, 1)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 1)

    def test_cleanup(self):
        """Test calling the run function twice, second time as cleanup. The
        run_failed state is reset for each call to run.

        """

        sequencer = Sequencer("cleanup")

        sequencer.run(FailTest("1"))
        passed, failed, skipped = sequencer.run(NamedTest("cleanup"))

        sequencer.report()

        self.assertEqual(passed, 1)
        self.assertEqual(failed, 1)
        self.assertEqual(skipped, 0)

        self.assertEqual(NamedTest.count, 1)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 1)

    def test_setup_teardown(self):
        """Test the setup and teardown methods.

        """

        sequencer = Sequencer("setup_teardown")

        result = sequencer.run(
            FailSetupTest("1"),
            FailTearDownTest("1")
        )

        sequencer.report()

        self.assertEqual(result, (0, 2, 0))
        self.assertEqual(FailSetupTest.count, 1)
        self.assertEqual(FailTearDownTest.count, 1)

    def test_asserts(self):
        """Test the various asserts.

        """

        sequencer = Sequencer("asserts")

        result = sequencer.run(
            FailAssertRaisesNoExceptionTest(),
            FailAssertRaisesWrongExceptionTest(),
            FailAssertIsNoneTest()
        )

        sequencer.report()

        self.assertEqual(result, (0, 3, 0))

    def test_testcase_description(self):
        """Test the testcase descriptions.

        """

        sequencer = Sequencer("testcase descriptions")

        result = sequencer.run(
            DescriptionNoneTest(),
            DescriptionEmptyTest(),
            DescriptionBlankTest(),
            DescriptionMultiLineTest()
        )

        sequencer.report()

        self.assertEqual(result, (4, 0, 0))

        json_report = sequencer.summary_json()
        self.assertEqual(json_report["testcases"][0]['description'], [])
        self.assertEqual(json_report["testcases"][1]['description'], [])
        self.assertEqual(json_report["testcases"][2]['description'], [])
        self.assertEqual(json_report["testcases"][3]['description'],
                         [
                             'Line 1.',
                             'Line 2.',
                             'Line 3.'
                         ])

    def test_execute_test_twice_two_run(self):
        """Execute the same test twice in two separate calls to run. This
        tests that a DOT graph can be created if multiple tests have
        the same name.

        """

        sequencer = Sequencer("execute_test_twice")

        result = sequencer.run([
            NamedTest("1"),
            NamedTest("1")
        ])

        self.assertEqual(result, (2, 0, 0))

        result = sequencer.run([
            NamedTest("1"),
            NamedTest("1")
        ])

        self.assertEqual(result, (4, 0, 0))

        sequencer.report()

        self.assertEqual(NamedTest.count, 4)
        self.assertEqual(NotExecutedTest.count, 0)
        self.assertEqual(FailTest.count, 0)


systest.configure_logging()

if __name__ == '__main__':
    unittest.main()
