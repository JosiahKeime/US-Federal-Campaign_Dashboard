def get_disbur_att(data=None, office=None, year=None):
    if office:
        data = data[data['Cand_Office'] == office]
    if year:
        data = data[data['Cand_Election_Yr'] == year]
    data = data[['Total_Disbursement', 'Cand_Office_St']].groupby(['Cand_Office_St']).sum()
    return data