
from subprocess import run
from tempfile import NamedTemporaryFile

from sqlalchemy.sql.functions import count

from ch2.command.args import m, V, bootstrap_file
from ch2.config.personal import acooke
from ch2.squeal.tables.source import Source
from ch2.squeal.tables.statistic import StatisticJournalText, StatisticJournal, StatisticJournalFloat, Statistic, \
    StatisticJournalInteger, StatisticType
from ch2.squeal.tables.topic import TopicJournal, Topic
from ch2.stoats.calculate.summary import SummaryStatistics


# the idea here is to test the new database schema with sources etc
# so we configure a database then load some data, calculate some stats,
# and see if everything works as expected.


def test_sources():

    with NamedTemporaryFile() as f:

        args, log, db = bootstrap_file(f, m(V), '5', configurator=acooke)

        with db.session_context() as s:

            # add a diary entry

            diary = s.query(Topic).filter(Topic.name == 'Diary').one()
            d = TopicJournal(topic=diary, time='2018-09-29')
            s.add(d)
            assert len(d.topic.fields) == 6, d.topic.fields
            assert d.topic.fields[0].statistic.name == 'Notes'
            assert d.topic.fields[1].statistic.name == 'Rest HR'
            for field in d.topic.fields:
                assert d.statistics[field].value is None
            d.statistics[d.topic.fields[0]].value = 'hello world'
            d.statistics[d.topic.fields[1]].value = 60

        with db.session_context() as s:

            # check the diary entry was persisted

            diary = s.query(Topic).filter(Topic.name == 'Diary').one()
            d = s.query(TopicJournal).filter(TopicJournal.topic == diary,
                                             TopicJournal.time == '2018-09-29').one()
            assert len(d.topic.fields) == 6
            assert d.topic.fields[0].statistic.name == 'Notes'
            assert d.statistics[d.topic.fields[0]].value == 'hello world'
            assert d.topic.fields[1].statistic.name == 'Rest HR'
            assert d.statistics[d.topic.fields[1]].value == 60
            assert d.statistics[d.topic.fields[1]].type == StatisticType.INTEGER

        # generate summary stats

        process = SummaryStatistics(log, db)
        process.run()

        with db.session_context() as s:

            # check the summary stats

            diary = s.query(Topic).filter(Topic.name == 'Diary').one()
            sleep = s.query(StatisticJournalInteger).join(Statistic). \
                filter(Statistic.owner == diary, Statistic.name == 'Rest HR').one()
            assert sleep.value == 60
            assert len(sleep.measures) == 2
            assert sleep.measures[0].rank == 1
            assert sleep.measures[0].percentile == 0
            n = s.query(count(StatisticJournalFloat.id)).scalar()
            assert n == 4, n
            n = s.query(count(StatisticJournalInteger.id)).scalar()
            assert n == 2, n
            m_avg = s.query(StatisticJournalFloat).join(Statistic). \
                filter(Statistic.name == 'Avg/Month Rest HR').one()
            assert m_avg.value == 60
            # note this is float even though Rest HR is int
            y_avg = s.query(StatisticJournalFloat).join(Statistic). \
                filter(Statistic.name == 'Avg/Year Rest HR').one()
            assert y_avg.value == 60

        with db.session_context() as s:

            # delete the diary entry

            diary = s.query(Topic).filter(Topic.name == 'Diary').one()
            d = s.query(TopicJournal).filter(TopicJournal.topic == diary,
                                             TopicJournal.time == '2018-09-29').one()
            s.delete(d)

        run('sqlite3 %s ".dump"' % f.name, shell=True)

        with db.session_context() as s:

            # check the delete cascade

            assert s.query(count(TopicJournal.id)).scalar() == 0
            # this should be zero because the Intervals were automatically deleted
            assert s.query(count(Source.id)).scalar() == 0
            assert s.query(count(StatisticJournalText.id)).scalar() == 0
            assert s.query(count(StatisticJournal.id)).scalar() == 0
