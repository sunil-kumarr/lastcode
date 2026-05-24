from lastcode.home import HomeWidget


def test_all_topic_deduplicates_problem_titles():
    widget = HomeWidget()
    widget._topic = "all"
    widget._difficulty = "all"
    widget._search_query = ""

    filtered = widget._filtered_and_sorted()
    titles = [problem["title"] for problem in filtered]

    assert len(titles) == len(set(title.lower() for title in titles))


def test_topic_filter_keeps_topic_specific_entries():
    widget = HomeWidget()
    widget._topic = "dp"
    widget._difficulty = "all"
    widget._search_query = ""

    filtered = widget._filtered_and_sorted()

    assert filtered
    assert all(problem["topic"] == "dp" for problem in filtered)
