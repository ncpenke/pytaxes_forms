from form import Form, FilingStatus

class F1040sa(Form):
    def __init__(f, inputs, f1040):
        super(F1040sa, f).__init__(inputs)
        if f['1']:
            f['2'] = f1040['38']
            # TODO: 7.5% if born before January 2, 1950
            f['3'] = f['2'] * .075
            f['4'] = max(0, f['1'] - f['3'])
        f['5'] = inputs['state_withholding'] + \
                 inputs.get('estimated_state_tax_payments', 0)
        f['9'] = max(f.rowsum(['5', '6', '7', '8']), 10000)
        f['15'] = f.rowsum(['10', '11', '12', '13', '14'])
        f['19'] = f.rowsum(['16', '17', '18'])
        f['29'] = f.rowsum(['9,', '19', '20'])
        f.must_file = True

    def title(self):
        return 'Schedule A'
