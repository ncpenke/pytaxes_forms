from form import Form, FilingStatus
from f1040 import F1040
import math

class MNm1m(Form):
    INCOME_LIMITS = [ 186350, 186350, 93175, 186350, 186350 ]
    INCOME_LIMITS_2 = [ 186350, 279500, 139750, 232900, 279500 ]
    INCOME_THRESHOLD_2 = [ 122500, 122500, 61250, 122500, 122500 ]
    INCOME_MULTIPLIER = [ 1550, 1250, 1250, 1550, 1250 ]
    
    def __line1__(f, inputs, m1, f1040):
        f1040sa = f1040.f1040sa
        w = Form({'disable_rounding':True})
        w.__title__ = "Worksheet for Line 1"
        w['1'] = f1040sa.rowsum(['4', '9', '15', '19', '20', '27', '28'])
        w['2'] = f1040sa.rowsum(['4', '14', '20', '28'])
        if w['2'] is None:
            w['2'] = 0 
        w['3'] = max(0, w['1'] - w['2'])
        if w['3'] <= 0:
            return 0
        w['4'] = w['3'] * .8
        w['5'] = f1040['37']
        w['6'] = f.INCOME_LIMITS[inputs['status']]
        w['7'] = max(0, w['5'] - w['6'])
        if w['7'] <= 0:
            return 0
        w['8'] = w['7'] * .03
        w['9'] = min(w['4'], w['8'])
        w['10'] = m1['2']
        w['11'] = w['9'] + w['10']
        w['12'] = w['1']
        w['13'] = F1040.STD_DED[inputs['status']]
        w['14'] = f1040.get('39a')
        if w['14'] is None:
            w['14'] = 0
        w['15'] = w['14'] * f.INCOME_MULTIPLIER[inputs['status']]
        w['16'] = w['13'] + w['15'] 
        w['17'] = max(0, w['12'] - w['16'])
        if w['17'] <= 0:
            return 0
        w['18'] = w['1']
        if w['11'] <= w['17']:
            w['19'] = w['18'] - w['9']
        else:
            w['19'] = w['18'] - (w['17'] - w['10'])
        w['20'] = f1040['40']
        return  w['20'] - w['19']

    def __line2__(f, inputs, m1, f1040):
        w = {}
        w['1'] = f1040['6d'] * 4050
        w['2'] = f1040['37']
        w['3'] = f.INCOME_LIMITS_2[inputs['status']]
        w['4'] = w['2'] - w['3']
        if w['4'] <= f.INCOME_THRESHOLD_2[inputs['status']]:
            divisor = 1250.0 if inputs['status'] == FilingStatus.SEPARATE else 2500.0 
            w['5'] = math.ceil(w['4'] / divisor)
            w['6'] = w['5'] * .02
            w['7'] = w['1'] * w['6']
        else:
            w['7'] = w['1']
        w['8'] = w['1'] - w['7'] 
        w['9'] = f1040['42']
        w['10'] = w['9'] - w['8']
        return w['10']
        
    def __init__(f, inputs, m1, f1040):
        super(MNm1m, f).__init__(inputs)
        f.must_file = True
        f['1'] = f.__line1__(inputs, m1, f1040)
        f['2'] = f.__line2__(inputs, m1, f1040) 
        # TODO: municipal bonds of another state
        # TODO: tax-exempt dividends in bonds of another state
        # TODO: federal bonus depreciation addition
        # TODO: expensing addition
        # TODO: S corp pass thru
        f['17'] = f.rowsum([("'" + str(i) + "'") for i in range(1,17)])
        f['44'] = 0

    def title(self):
        return '2018 Schedule M1M, Income Additions and Subtractions'
