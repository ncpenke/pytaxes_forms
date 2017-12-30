from form import Form, FilingStatus

class F8801(Form):
    """Form 8801, Credit for Prior Year Minimum Tax"""
    def __init__(f, inputs, f1040, f6251):
        super(F8801, f).__init__(inputs)

        pf6251 = inputs.get('prev_F6251')

        if pf6251 is not None:
            EXEMPTIONS = [53900, 83800, 41900, 53900, 83800]
            EXEMPT_LIMITS = [119700, 159700, 79850, 119700, 159700]
            RATE_CHANGE = [186300, 186300, 93150, 186300, 186300]
            RATE_OFFSET = [3726, 3726, 1863, 3726, 3726]

            f['1'] = pf6251.rowsum(['1', '6', '10'])
            f['2'] = pf6251.rowsum(['2', '3', '4', '5', '7', '9', '12', '13'])
            f['4'] = max(pf6251.rowsum(['1', '2', '3']), 0)
            status = inputs['status']
            if (f.get('4') > 247450 and status == FilingStatus.SEPARATE):
                raise RuntimeError('TODO: Excess income while filing separate')
            f['5'] = EXEMPTIONS[status]
            f['6'] = EXEMPT_LIMITS[status]
            f['7'] = max(f.get('4') - f.get('6'), 0)
            f['8'] = 0.25 * f.get('7')
            f['9'] = max(f.get('5') - f.get('8'), 0)
            f['10'] = f.get('4') - f.get('9')
            if (f.get('10') <= RATE_CHANGE[status]):
                f['11'] = f['10'] * .26
            else:
                f['11'] = f['10'] * 0.28 - RATE_OFFSET[status]
            f['12'] = 0
            f['13'] = f.get('11') - f.get('12')
            f['14'] = pf6251.get('34')
            f['15'] = max(f.get('13') - f.get('14'), 0)
            f['16'] = pf6251.get('35')
            f['17'] = f.get('15')
            f['18'] = f.get('16') - f.get('17')
            f['19'] = inputs.get('prior_amt_credit')
            f['21'] = f.rowsum(['18', '19', '20'])
        else:
            f['21'] = inputs.get('prior_amt_credit')
            if not f['21']:
                return

        f.must_file = True
        f['22'] = max(0, f1040['44'] + f1040['46'] - \
            (f1040.rowsum(['48', '49', '50', '51', '52', '53', '54']) or 0))
        f['23'] = f6251.get('33')
        f['24'] = max(0, f['22'] - f['23'])
        f.comment['25'] = 'Minimum tax credit'
        f['25'] = min(f['21'], f['24'])
        if f['25']:
            f6251.must_file = True
        f.comment['26'] = 'Credit carryforward to 2018'
        f['26'] = f['21'] - f['25']

    def title(self):
        return 'Form 8801 (for 2017 filing)'
