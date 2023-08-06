
## Poller Package

"""
    Base class for classes that polls a task regularly, with a constant minimum time interval between each poll.
    Warning: Each polling interval is the maximum of a) polling_interval_secs and b) the time taken to do the task.
            (so the polling interval might be longer than polling_interval_secs
    ToDo: An alternative name might be ScheduledTask

    """


    def __init__(self):
        """
            Construct a new Poller object (Poller is an abstract class)
        """



    @abstractmethod
    def do_work(self):
        """
            Perform the work to be done, during each poll (aka 'scheduled task')

            :raises This procedure must be overridden or it will raise a NotImplemenetedError

        """


    def start(self, polling_interval_secs=DEFAULT_INTERVAL):
        """
            Start (or re-start) the poller. This will run the do_work procedure every self.polling_interval_secs seconds
            If the do_work procedure takes longer than polling_interval_secs, the next poll will take place as
            soon as the task has finished:
                Each polling interval is the maximum of a) polling_interval_secs and b) the time taken to do the task.

            :param polling_interval_secs: time interval (seconds) between scheduled runs.
            :raises polling_interval_secs must be greater than 0 or a ValueError will be returned.
            :type polling_interval_secs: float

        """

        

    def stop(self):
        """
            Stop the poller. if it is running. If none is running, do nothing.

        """

