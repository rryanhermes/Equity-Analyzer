import math
import scipy.stats as scipy
import statistics


def calculateMeanCI(size, confidence, mean, sd):
    if size < 30:
        se = sd / math.sqrt(size)
        mfe = se * scipy.t.ppf((1 - (confidence / 100)) / 2, size - 1)
        upper = round(mean + mfe, 3)
        lower = round(mean - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')

    elif size >= 30:
        z = {'75': 1.15,
             '90': 1.645,
             '95': 1.959,
             '97': 2.17,
             '99': 2.576,
             '99.9': 3.29
             }

        se = sd / math.sqrt(size)
        mfe = se * z[str(confidence)]
        upper = round(mean + mfe, 3)
        lower = round(mean - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')


def calculateMeanCIdata(data, confidence):
    size = len(data)
    mean = statistics.mean(data)
    sd = statistics.pstdev(data)

    if size < 30:
        se = sd / math.sqrt(size)
        mfe = se * scipy.t.ppf((1 - (confidence / 100)) / 2, size - 1)
        upper = round(mean + mfe, 3)
        lower = round(mean - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')

    elif size >= 30:
        z = {'75': 1.15,
             '90': 1.645,
             '95': 1.959,
             '97': 2.17,
             '99': 2.576,
             '99.9': 3.29
             }

        se = sd / math.sqrt(size)
        mfe = se * z[str(confidence)]
        upper = round(mean + mfe, 3)
        lower = round(mean - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')


def calculateProportionCI(size, confidence, x):
    p = x / size
    q = 1 - p

    if size * p < 15 or size * q < 15:
        z = {'75': 1.15,
             '90': 1.645,
             '95': 1.959,
             '97': 2.17,
             '99': 2.576,
             '99.9': 3.29
             }
        p = ((p * size) + 2) / (size + 4)
        q = 1 - p
        se = math.sqrt((p * q) / (size + 4))
        print(se)
        mfe = se * z[str(confidence)]
        upper = round(p + mfe, 3)
        lower = round(p - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')

    elif size * p > 15 and size * q > 15:
        z = {'75': 1.15,
             '90': 1.645,
             '95': 1.959,
             '97': 2.17,
             '99': 2.576,
             '99.9': 3.29
             }
        se = math.sqrt(((p * q) / size))
        mfe = se * z[str(confidence)]
        upper = round(p + mfe, 3)
        lower = round(p - mfe, 3)

        print(f'Lower: {lower}, Upper: {upper}')


# calculateMeanCIdata(data, 95)
#
# calculateProportionCI(
#     size=100,
#     confidence=99.9,
#     x=50,
# )
#
# calculateMeanCI(
#     size=1000,
#     mean=1000,
#     sd=100,
#     confidence=99,
# )

calculateMeanCI(237, 90, 409, 68)