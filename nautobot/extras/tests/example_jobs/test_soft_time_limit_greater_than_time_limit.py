from nautobot.extras.jobs import Job


class TestSoftTimeLimitExceeded(Job):
    class Meta:
        name = "Soft Time Limit Greater Than Hard Time Limit"
        soft_time_limit = 10
        time_limit = 5

    def run(self, data, commit):
        return "Finished"
