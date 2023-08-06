
from ..command.args import parser, NamespaceWithVariables, NO_OP
from ..lib.log import make_log
from ..squeal.database import Database
from ..squeal.tables.activity import Activity
from ..squeal.tables.constant import Constant
from ..squeal.tables.pipeline import Pipeline, PipelineType
from ..squeal.tables.statistic import Statistic, StatisticType
from ..squeal.tables.topic import Topic, TopicField
from ..uweird.fields import Integer


def config(*args):
    '''
    Start here to configure the system.  Create an instance on the command line:

        log, db = config('-v', '4')
        print(c...)  todo
        ...
    '''
    if len(args) == 1:
        args = args[0].split(' ')
    p = parser()
    args = list(args)
    args.append(NO_OP)
    ns = NamespaceWithVariables(p.parse_args(args))
    log = make_log(ns)
    db = Database(ns, log)
    return log, db


class Counter:

    def __init__(self, start=10, delta=10):
        self.__start = start
        self.__delta = delta
        self.__previous = None

    def __call__(self, reset=None, delta=None):
        if delta is not None:
            if delta < 1:
                raise Exception('Negative increment')
            self.__delta = delta
        if reset is None:
            if self.__previous is None:
                self.__previous = self.__start
            else:
                self.__previous += self.__delta
        else:
            if reset <= self.__previous:
                raise Exception('Sort not increasing with reset')
            else:
                self.__previous = reset
        return self.__previous


def add(session, instance):
    '''
    Add an instance to the session (and so to the database), returning the instance.
    You likely don't need this - see the more specific helpers below.

    The instance can of any class that subclasses the Base class from SQLAlchemy.
    In practice, that means most classes in the ch2.squeal.tables mdoule.
    However, only some classes make sense in the context of a configuration, and
    more specific helpers probably already exist for those.
    '''
    session.add(instance)
    return instance


def add_statistics(session, cls, sort, **kargs):
    '''
    Add a class to the statistics pipeline.

    The pipeline classes are invoked when the diary is modified and when activities are added.
    They detect new data and calculate appropriate statistics.
    See the ch2.stoats module for examples.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(session, Pipeline(cls=cls, type=PipelineType.STATISTIC, sort=sort, kargs=kargs))


def add_diary(session, cls, sort, **kargs):
    '''
    Add a class to the diary pipeline.

    The pipeline classes are invoked when the diary is displyed.
    They generate display classes for activity statistics (and similar)
    See the ch2.stoats module for examples.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(session, Pipeline(cls=cls, type=PipelineType.DIARY, sort=sort, kargs=kargs))


def add_monitor(session, cls, sort, **kargs):
    '''
    Add a class to the monitor pipeline.

    The pipeline classes are invoked when activities are imported from FIT files.
    They read the files and create MonitorJournal entries and associated statistics.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(session, Pipeline(cls=cls, type=PipelineType.MONITOR, sort=sort, kargs=kargs))


def add_activity(session, name, sort, description=None):
    '''
    Add an activity type to the configuration.

    These are used to group activities (and related statistics).
    So typical entries might be for cycling, running, etc.
    '''
    return add(session, Activity(name=name, sort=sort, description=description))


def add_activities(session, cls, sort, **kargs):
    '''
    Add a class to the activities pipeline.

    The pipeline classes are invoked when activities are imported from FIT files.
    They read the files and create ActivityJournal entries and associated statistics.

    The sort argument fixes the order in which the classes are instantiated and called and can
    be an integer or a callable (that returns an integer) like Counter above.

    The kargs are passed to the constructor and so can be used to customize the processing.
    '''
    return add(session, Pipeline(cls=cls, type=PipelineType.ACTIVITY, sort=sort, kargs=kargs))


def add_activity_constant(session, activity, name, description=None, units=None, type=StatisticType.INTEGER):
    '''
    Add a constant associated with an activity.

    Configuring a constant allows the user to supply a value later, using the `ch2 constant` command.
    This can be useful for values that don't vary often, and so aren't worth adding to the diary.
    An example is FTHR, which you will only measure occasionally, but which is needed when calculating
    activity statistics (also, FTHR can vary by activity, which is why we add a constant per activity).
    '''
    if activity.id is None:
        session.flush()
    statistic = add(session, Statistic(name=name, owner=Constant, constraint=activity.id, units=units,
                                       description=description))
    constant = add(session, Constant(type=type, name='%s.%s' % (name, activity.name), statistic=statistic))


def add_topic(session, name, sort, description=None, schedule=None):
    '''
    Add a root topic.

    Topics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A root topic is usually used as a header to group related children.
    For example, 'Diary' to group diary entries (notes, weight, sleep etc), or 'Plan' to group training plans.
    '''
    return add(session, Topic(name=name, sort=sort, description=description, schedule=schedule))


def add_child_topic(session, parent, name, sort, description=None, schedule=None):
    '''
    Add a child topic.

    Topics are displayed in the diary.
    They can be permanent, or associated with some schedule.
    They can also be associated with fields (and so with statistics).

    A child topic is used to add additional structrure to an existing topic.
    For example, the parent topic might be "injuries" and permanent, while children are defined for
    specific injuries with a schedule that gives start and end dates.
    '''
    return add(session, Topic(parent=parent, name=name, sort=sort, description=description, schedule=schedule))


def add_topic_field(session, topic, name, sort, description=None, units=None, summary=None,
                    display_cls=Integer, **display_kargs):
    '''
    Add a field and associated statistic to a topic entry.

    This is how the user can enter values into the diary.
    The field describes how the values are displayed in the diary.
    The statistic describes how the values are stored in the database.
    '''
    if topic.id is None:
        session.flush()
    statistic = add(session, Statistic(name=name, owner=topic, constraint=topic.id,
                                       description=description, units=units, summary=summary))
    field = add(session, TopicField(topic=topic, sort=sort, type=display_cls.statistic_type,
                                    display_cls=display_cls, display_kargs=display_kargs,
                                    statistic=statistic))
