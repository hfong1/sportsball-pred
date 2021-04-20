import bnlearn


class Bnet():

    def __init__(self, game):
        self.game = game
        game.setStats()
        game.getAllGames()
        pdf = game.convert_ops_era_to_df()
        pdf = pdf.astype(float)
        # OPS = pdf.drop(columns=['Pera(D)', 'Wera(D)'])

        pdf['Pops(A)'] = (pdf['Pops(A)'] * 10)
        pdf['Wops(A)'] = (pdf['Wops(A)'] * 10)
        pdf['Wera(D)'] = ((pdf['Wera(D)'] * -1) + 5)
        pdf['Pera(D)'] = ((pdf['Pera(D)'] * -1) + 5)

        pdf['Pops(A)'] = pdf['Pops(A)'].apply(lambda x: round(x))
        pdf['Wops(A)'] = pdf['Wops(A)'].apply(lambda x: round(x))
        pdf['Pera(D)'] = pdf['Pera(D)'].apply(lambda x: round(x))
        pdf['Wera(D)'] = pdf['Wera(D)'].apply(lambda x: round(x))

        self.wops_range = self.minmax(pdf['Wops(A)'])
        self.pops_range = self.minmax(pdf['Pops(A)'])
        self.wera_range = self.minmax(pdf['Wera(D)'])

        pdf = pdf.rename(columns={"winsW": "WinsW"})

        edges = [
            ('Pops(A)', 'WinsW'),
            ('Wops(A)', 'WinsW'),
            ('Pera(D)', 'WinsW'),
            ('Wera(D)', 'WinsW'),
            ('Pera(D)', 'Wera(D)'),
            ('Wops(A)', 'Pops(A)'),
        ]

        self.DAG = bnlearn.make_DAG(edges)
        self.DAG = bnlearn.parameter_learning.fit(self.DAG, pdf, methodtype='bayes', verbose=1)

    def get_ranges(self):
        ranges = {
            'wops': self.wops_range,
            'pops': self.pops_range,
            'wera': self.wera_range,
        }

        return ranges

    def get_bnet_wr(self, wops=1, pops=1, wera=1):
        Pera = round(((9.00/10 * -1) + 1) * 10)
        Wera = round(((8.00/10 * -1) + 1) * 10)
        q1 = bnlearn.inference.fit(
            self.DAG,
            variables=['WinsW'],
            evidence={'Wops(A)': wops, 'Pops(A)': pops, 'Wera(D)': wera},
            verbose=1
        )
        return q1.values[0]

    @staticmethod
    def minmax(val_list):
        min_val = min(val_list)
        max_val = max(val_list)

        return min_val, max_val
