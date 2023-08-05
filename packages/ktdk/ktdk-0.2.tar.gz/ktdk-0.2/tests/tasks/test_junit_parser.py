import pytest

from ktdk.core.tests import Test
from ktdk.tasks.xunit.junit import JUnitParseTask
from tests.utils import get_test_context

JUNIT_SUCCESS = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="testbomb" errors="0" failures="0" tests="319" hostname="tbd" time="0.014154" timestamp="2018-03-02T09:00:01Z">
    <testcase classname="testbomb.global" name="Basic player actions/Move down, no obstacles there" time="0.000078"/>
    <testcase classname="testbomb.global" name="Basic player actions/Move left, stop on border" time="0.000053"/>
    <testcase classname="testbomb.global" name="Basic player actions/Drop a bomb" time="0.000028"/>
    <testcase classname="testbomb.Fixture" name="Game objects correctly implement visit() methods" time="0.000111"/>
    <testcase classname="testbomb.Fixture" name="Game object texture get/set" time="0.000045"/>
    <testcase classname="testbomb.Fixture" name="Scenario: It is possible to create obstacles/Given: An empty map/When: a brick is created/Then: a wall is on the map" time="0.000014"/>
    <testcase classname="testbomb.Fixture" name="Scenario: It is possible to create obstacles/Given: An empty map/When: A stone is created/Then: a wall is on the map" time="0.000011"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Which objects blocks player movement?/Given: A player alongside a wall/When: The player goes towards the obstacle/Then: He does not move at all" time="0.000034"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Which objects blocks player movement?/Given: A player alongside a bomb/When: The player goes towards the obstacle/Then: He does not move at all" time="0.000019"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Which objects blocks player movement?/Given: A player alongside another player/When: The player goes towards the other player/Then: They end up standing on the same position" time="0.000021"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Player can drop a bomb on an unaligned position" time="0.000122"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Player can pick up a bonus/Given: Player standing next to a bonus item" time="0.000067"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Player can land bombs/Given: A player with bomb limit = 1/When: The player lands a bomb/And when: The bomb explodes/Then: The player can land another bomb" time="0.000286"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Player can land bombs/Given: Two players with bomb limit = 1/When: one player lands a bomb/Then: the other player can land a bomb, too" time="0.000009"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bomb explosion/Given: A newly planted bomb" time="0.000265"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bomb explosion/Given: A newly planted bomb/When: The time is almost out/Then: The bomb is still there" time="0.000003"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bomb explosion/Given: A newly planted bomb/When: The time is out/Then: The bomb is no longer there" time="0.000042"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bomb explosion/Given: A newly planted bomb/When: The time is out/Then: The bomb is no longer there/And: there is some fire around" time="0.000031"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bonus item does not stop fire/Given: A bomb with range=2, a bonus item nearby/When: the bomb explodes" time="0.000259"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bonus item does not stop fire/Given: A bomb with range=2, a bonus item nearby/When: the bomb explodes/Then: there is a fire on place of the bonus, and behind the bonus" time="0.000008"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Brick does not fire/Given: A bomb with range=2, a brick wall nearby/When: the bomb explodes" time="0.000257"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Brick does not fire/Given: A bomb with range=2, a brick wall nearby/When: the bomb explodes/Then: there is no fire neither on place of the wall nor behind the wall" time="0.00001"/>
    <testcase classname="testbomb.Fixture" name="Scenario: Bonus::BombMax/Given: A player with no bonus/When: the player eats Bonus::BombMax/And when: the player tries to land all 2 bombs to the same cell/Then: well, there is a bomb in the cell/And: but the player can still land another one bomb somewhere else" time="0.000013"/>
    <system-out/>
    <system-err/>
  </testsuite>
</testsuites>
"""

JUNIT_FAIL = """<?xml version="1.0" encoding="UTF-8"?>
<testsuites>
  <testsuite name="hw02_tests" errors="0" failures="17" tests="17" hostname="tbd" time="0.00183" timestamp="2018-03-02T13:50:27Z">
    <testcase classname="Read file, simple options" name="root" time="0.000017">
      <system-err>
Unable to open provided file inputs/basic.txt
Unable to open provided file empty
      </system-err>
    </testcase>
    <testcase classname="Read file, simple options" name="simple" time="0.00011">
      <failure message="3 == 0" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:16
      </failure>
    </testcase>
    <testcase classname="Read file, simple options" name="Not existing file" time="0.000046">
      <failure message="0 == 3" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:23
      </failure>
    </testcase>
    <testcase classname="Read file, simple options" name="Empty file" time="0.000048">
      <failure message="3 == 0" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:35
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="root" time="0.00003">
      <system-err>
Unable to open provided file inputs/wrong1.txt
Unable to open provided file inputs/basic.txt
      </system-err>
    </testcase>
    <testcase classname="Read file, options" name="No permission" time="0.000037">
      <failure message="0 == 3" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:51
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: missing =" time="0.000064">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:62
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: missing ]" time="0.000031">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:66
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: Empty section name" time="0.000025">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:70
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: Empty value name" time="0.000032">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:74
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: Empty key name" time="0.000036">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:78
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: key=value before first section" time="0.000037">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:82
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: Empty value name" time="0.000043">
      <failure message="3 == 4" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:86
      </failure>
    </testcase>
    <testcase classname="Read file, options" name="Wrong: key=value before first section, not empty config" time="0.000037">
      <failure message="3 == 0" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:90
      </failure>
    </testcase>
    <testcase classname="Parsing basic file" name="root" time="0.000029">
      <system-err>
Unable to open provided file inputs/basic.txt
Unable to open provided file inputs/basic.txt
      </system-err>
    </testcase>
    <testcase classname="Parsing basic file" name="has Section" time="0.00002">
      <failure message="false" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:100
      </failure>
    </testcase>
    <testcase classname="Parsing basic file" name="has Key" time="0.000021">
      <failure message="false" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:107
      </failure>
    </testcase>
    <testcase classname="Parsing basic file" name="value" time="0.00003">
      <failure message="1 == 0" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:119
      </failure>
    </testcase>
    <testcase classname="Parsing basic file" name="isValue" time="0.000031">
      <failure message="false" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:137
      </failure>
    </testcase>
    <testcase classname="Parsing basic file" name="hasValue" time="0.000037">
      <failure message="false" type="REQUIRE">
at /tmp/hw02/solution/basic.cpp:149
      </failure>
    </testcase>
    <system-out/>
    <system-err>
Unable to open provided file inputs/basic.txt
Unable to open provided file empty
    </system-err>
  </testsuite>
</testsuites>
"""


def create_junit(out_dir, name, content):
    file_name = name + '.xml'
    out_dir = out_dir / 'results'
    junit = out_dir.join(file_name)
    junit.write(content)
    return str(junit)


@pytest.fixture()
def workspace(tmpdir):
    path = tmpdir.mkdir('workspace')
    path.mkdir('results')
    return path


@pytest.fixture()
def context(workspace):
    config = dict(workspace=workspace)
    return get_test_context(suite_config=config)


@pytest.fixture()
def succ_junit(workspace):
    return create_junit(workspace, 'succ', JUNIT_SUCCESS)


@pytest.fixture()
def fail_junit(workspace):
    return create_junit(workspace, 'fail', JUNIT_FAIL)


def test_should_parse_succ_junit(context, succ_junit):
    junit_file = succ_junit
    suites = JUnitParseTask(junit_file=junit_file)
    root_test = Test(name="root")
    root_test.add_task(suites)
    runner = root_test.runner.get_instance(context=context)
    runner.invoke()
    assert root_test.result.effective.passed


def test_should_parse_fail_junit(context, fail_junit):
    junit_file = fail_junit
    suites = JUnitParseTask(junit_file=junit_file)
    root_test = Test(name="root")
    root_test.add_task(suites)
    runner = root_test.runner.get_instance(context=context)
    runner.invoke()
    assert root_test.result.effective.failed
