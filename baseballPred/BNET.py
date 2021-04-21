import bnlearn


def get_bn_winrate(game, wops=1, pops=1):
    game.setStats()
    game.getAllGames()
    pdf = game.convert_ops_era_to_df()
    pdf = pdf.astype(float)
    OPS = pdf.drop(columns=['Pera(D)', 'Wera(D)'])

    pdf['Pops(A)'] = (pdf['Pops(A)'] * 10)
    pdf['Wops(A)'] = (pdf['Wops(A)'] * 10)
    pdf['Wera(D)'] = ((pdf['Wera(D)'] * -1) + 5)
    pdf['Pera(D)'] = ((pdf['Pera(D)'] * -1) + 5)

    pdf['Pops(A)'] = pdf['Pops(A)'].apply(lambda x: round((x)))
    pdf['Wops(A)'] = pdf['Wops(A)'].apply(lambda x: round((x)))
    pdf['Pera(D)'] = pdf['Pera(D)'].apply(lambda x: round((x)))
    pdf['Wera(D)'] = pdf['Wera(D)'].apply(lambda x: round((x)))

    pdf = pdf.rename(columns={"winsW": "WinsW"})

    edges = [
        ('Pops(A)', 'WinsW'),
        ('Wops(A)', 'WinsW'),
        ('Pera(D)', 'WinsW'),
        ('Wera(D)', 'WinsW'),
        ('Pera(D)', 'Wera(D)'),
        ('Wops(A)', 'Pops(A)'),
    ]

    DAG = bnlearn.make_DAG(edges)
    df = bnlearn.sampling(DAG, n=100)
    DAG = bnlearn.parameter_learning.fit(DAG, pdf, methodtype='bayes', verbose=1)
    DAG_true = bnlearn.import_DAG()

    Pera = round(((9.00/10 * -1) + 1) * 10)
    Wera = round(((8.00/10 * -1) + 1) * 10)
    q1 = bnlearn.inference.fit(
        DAG,
        variables=['WinsW'],
        evidence={'Wops(A)': wops, 'Pops(A)': pops, 'Wera(D)': 1},
        verbose=1
    )
    return q1.values[0]
