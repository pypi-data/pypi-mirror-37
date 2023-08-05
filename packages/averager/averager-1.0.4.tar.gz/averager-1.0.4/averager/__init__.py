class Averager:

    def average(*numbers):
        average = sum(numbers) / len(numbers)
        if average == int(average):
            return int(average)
        else:
            return average


class WeightedAverager(Averager):

    def __init__(self, **weights):
        for weight in weights:
            if weights[weight] < 0:
                raise ValueError("Weights cannot be less than zero.")
        self.weights = weights

    def average(self, **numbers):
        dividend = 0.0
        divisor = 0
        for name in numbers:
            number = numbers[name]
            if name in self.weights:
                weight = self.weights[name]
            else:
                raise ValueError("Weight for {} not defined.".format(name))
            dividend += number * weight
            divisor += weight
        average = dividend / divisor
        if average == int(average):
            return int(average)
        else:
            return average
