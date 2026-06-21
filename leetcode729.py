# 729. My Calendar I

class MyCalendar(object):

    def __init__(self):
        self.events = []

    def book(self, startTime, endTime):
        for start, end in self.events:
            if startTime < end and endTime > start:
                return False

        self.events.append((startTime, endTime))
        return True

# Your MyCalendar object will be instantiated and called as such:
# obj = MyCalendar()
# param_1 = obj.book(startTime,endTime)

