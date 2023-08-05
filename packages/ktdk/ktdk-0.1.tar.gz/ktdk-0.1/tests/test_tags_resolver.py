from ktdk.runtime.tags import TagsEvaluator


def get_evaluator(expr):
    resolver = TagsEvaluator(expr)
    resolver.register_tags('hello', 'world', 'naostro', 'nanecisto')
    return resolver


def test_tags_evaluator_empty():
    resolver = get_evaluator("")
    assert resolver.evaluate()
    assert resolver.evaluate('hello', 'world')
    assert resolver.evaluate("hello")


def test_tags_evaluator_simple_only_naostro():
    resolver = get_evaluator("naostro")
    assert resolver.evaluate("naostro")
    assert resolver.evaluate("naostro", "nanecisto")
    assert not resolver.evaluate("nanecisto")
    assert not resolver.evaluate()


def test_tags_evaluator_simple_or():
    resolver = get_evaluator("naostro or nanecisto")
    assert resolver.evaluate("naostro", "nanecisto")
    assert resolver.evaluate("naostro", "nanecisto", 'world')
    assert resolver.evaluate("naostro")
    assert resolver.evaluate("nanecisto")
    assert not resolver.evaluate()
    assert not resolver.evaluate("hello", "world")


def test_tags_evaluator_simple_and():
    resolver = get_evaluator("naostro and nanecisto")
    assert not resolver.evaluate()
    assert not resolver.evaluate("nanecisto")
    assert not resolver.evaluate("naostro")
    assert not resolver.evaluate("hello", "world")
    assert resolver.evaluate("naostro", "nanecisto")


def test_tags_evaluator_simple_not():
    resolver = get_evaluator("not naostro")
    assert resolver.evaluate()
    assert resolver.evaluate("hello", "world")
    assert resolver.evaluate("nanecisto")
    assert not resolver.evaluate("naostro")
    assert not resolver.evaluate("naostro", "nanecisto")


def test_tags_evaluator_using_non_existing_tag_in_test_tags():
    resolver = get_evaluator("naostro")
    assert resolver.evaluate("naostro")
    assert not resolver.evaluate("foo")
    assert resolver.evaluate("naostro", "bar")


def test_tags_evaluator_using_non_existing_tag_in_the_expression():
    resolver = get_evaluator("foo")
    assert not resolver.evaluate()
    assert not resolver.evaluate("foo")
    assert not resolver.evaluate("naostro", "bar")
