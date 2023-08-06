from unittest import TestLoader, TestSuite
from HtmlTestRunner import HTMLTestRunner

test_bucket = TestLoader().discover(start_dir="svt", pattern="*spark*.py")

suite = TestSuite(test_bucket)
runner = HTMLTestRunner(
    combine_reports=True,
    add_timestamp=True,
    report_name="aios-python",
    report_title="AIOS Python Client"
)

runner.run(suite)
