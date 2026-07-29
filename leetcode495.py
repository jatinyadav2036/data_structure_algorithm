# 495. Teemo Attacking

class Solution(object):
    def findPoisonedDuration(self, timeSeries, duration):
        sm = 0
        for i in range(len(timeSeries)-1):
            if timeSeries[i] + duration <= timeSeries[i+1]:
                sm += duration
            else:
                sm += timeSeries[i+1] - timeSeries[i]
        sm += duration
        
        return sm