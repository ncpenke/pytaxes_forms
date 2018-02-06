from form import Form, FilingStatus
from f1040 import F1040
from mnm1m import *

class MNm1(Form):
    BRACKET_RATES = [ 0.0535, 0.0705, 0.0798, 0.0985 ]
    BRACKET_LIMITS = [
        [ 25390, 83400, 156900 ],
        [ 37110, 147450, 261510 ],
        [ 18560, 73730, 130760 ],
        [ 31260, 125600, 209200 ]
    ]
    
    def __init__(f, inputs, f1040):
        super(MNm1, f).__init__(inputs)
        f.must_file = True
        f.addForm(f)
        # TODO M1HOME
        f['1'] = f1040['43']
        f['2'] = f.__line2__(inputs, f1040.f1040sa)

        m1m = MNm1m(inputs, f, f1040)
        f.addForm(m1m)

        f['3'] = m1m['17']
        f['4'] = f.rowsum(['1','2','3'])
        f['5'] = f1040['10']
        f['6'] = m1m['44']
        f['7'] = f.rowsum(['5','6'])
        f.comment['8'] = "MN taxable income"
        f['8'] = f['4'] - f['7']
        f.comment['9'] = "MN tax"
        f['9'] = f.tax_worksheet(inputs['status'], f['8'])
        # TODO: M1MT
        f['10'] = 0
        f['11'] = f['9'] + f['10']
        # TODO: Part year and non residnts
        f['12'] = f['11']
        f['15'] = f.rowsum(['12', '13', '14'])
        f['20'] = f['15'] - f['19']
        f['22'] = f.rowsum(['20', '21'])
        # TODO: Tax on lump-sum distribution
        # TODO: M1CR and M!RCR
        f['23'] = inputs.get('state_withholding') 
        f['24'] = inputs.get('estimated_state_tax_payments') + inputs.get('extra_estimated_state_tax_payments')
        f['27'] = f.rowsum(['23', '24'])
        if f['27'] > f['22']:
            f.comment['28'] = 'MN refund'
            f['28'] = f['27'] - f['22']
        else:
            f.comment['30'] = 'MN owed'
            f['30'] = f['22'] - f['27']

    def __line2__(f, inputs, f1040sa):
        w = {}
        w['1'] = f1040sa['29']
        w['2'] = F1040.STD_DED[inputs['status']]
        w['3'] = max(w['1'] - w['2'], 0)
        w['4'] = f1040sa['5']
        return min(w['4'], w['3'])

    def tax_worksheet(f, status, val):
        # TODO: rounding of amounts less than 100000 to match tax table
        tax = 0
        prev = 0
        i = 0
        for lim in f.BRACKET_LIMITS[status]:
            if val <= lim:
                break
            tax += f.BRACKET_RATES[i] * (lim - prev)
            prev = lim
            i += 1
        tax += f.BRACKET_RATES[i] * (val - prev)
        return tax

    def title(self):
        return '2018 Form M1, Individual Income Tax'
