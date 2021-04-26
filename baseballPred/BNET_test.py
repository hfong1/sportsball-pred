import pandas as pd
import bnlearn
import GamesBetweenTeams

team_id_dict = {
    # National League 
    'Arizona Diamondbacks':109,
    'Chicago Cubs': 112,
    'Cincinnati Reds': 113,
    'Colorado Rockies':115,
    'Los Angeles Dodgers':119,
    'Washington Nationals':120,
    'New York Mets':121,
    'Pittsburgh Pirates':134,
    'San Diego Padres':135,
    'San Francisco Giants':137,
    'St. Louis Cardinals':138,
    'Philadelphia Phillies':143,
    'Atlanta Braves':144,
    'Miami Marlins':146,
    'Milwaukee Brewers':158,
}
def getError(team1, team2):
    print("Hello, World!")
    gamesObj = GamesBetweenTeams.getGamesBetweenTeams(team1, team2, '01/01/2016', '12/31/2018')
    gamesObj.setStats()
    gamesObj.getAllGames()
    print("And goodbye world!")
    pdf = gamesObj.convert_ops_era_to_df()
    pdf = pdf.astype(float)
    ax = pdf.plot.line()
    OPS = pdf.drop(columns=['Pera(D)', 'Wera(D)'])
    OPS.plot.line()

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
    df = bnlearn.sampling(DAG, n=len(gamesObj.games))
    DAG = bnlearn.parameter_learning.fit(DAG, pdf, methodtype='bayes', verbose=1)
    DAG_true = bnlearn.import_DAG()
    
    ops1= round(float(gamesObj.ops[0][-1])*10)
    ops2 = round(float(gamesObj.ops[1][-1])*10)
  
    era1 = round(((float(gamesObj.era[0][-1])/10 * -1) + 1) * 10)
    era2 = round(((float(gamesObj.era[1][-1])/10 * -1) + 1) * 10)
    try:
        q1 = bnlearn.inference.fit(
            DAG,
            variables=['WinsW'],
            evidence={'Wops(A)': ops1, 'Pops(A)': ops2, 'Wera(D)': era1},
            verbose=1
        )
        print(q1.values[0], q1.values[1])
        return q1.values[0]
    except IndexError:
        print("Lack of data")
        return 0.5

def main():
    l = []
    n = 0
    m = 0
    for i, elem in enumerate(team_id_dict):
        for j, elem2 in enumerate(team_id_dict):
            if (i < j):
                print("Current Teams:",elem, elem2)
                gameclass = GamesBetweenTeams.getGamesBetweenTeams(team_id_dict.get(elem), team_id_dict.get(elem2), '01/01/2019', '12/31/2019')
                wr1 = float(gameclass.getWinRate())
                wr2 = float(getError(team_id_dict.get(elem), team_id_dict.get(elem2)))
                print("Win Rate 1:",wr1 * 100)
                print("Win Rate 2:", wr2 * 100)
                l.append((wr2-wr1)/wr1)
    for item in l:
        print("Error: ", item * 100)
        n = n + 1
        m = m + item
    print("Final:", m/n)

if __name__ == "__main__":
    main()
