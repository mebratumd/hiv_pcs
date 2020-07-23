import pandas as pd
import scipy.stats as stats
import numpy as np
import os

def fisher(title,data,comp):

    # Fisher's exact to be used exclusively with population coverage data

    countries = ['Japan','South Korea','Mongolia','China','Hong Kong','Pakistan','India','Sri Lanka','Philippines','Singapore','Malaysia','Thailand','Vietnam','Taiwan','Indonesia','Israel','Oman','Lebanon','UAE','Saudi Arabia','Iran','Jordan','Croatia','England','France','Italy','Spain','Russia','Turkey','Austria','Bulgaria','Czech Republic','Poland','Romania','Scotland','United Kingdom','Kenya','Uganda','Zambia','Zimbabwe','Senegal','Ivory Coast','Burkina Faso','Cape Verde','Guinea Bissau','Sao Tome and Principe','Rwanda','Central African Republic','Cameroon','Morocco','Sudan','Mali','Tunisia','South Africa','Cuba','Guatemala','US','Argentina','Brazil','Chile','Ecuador','Peru','Venezuela','Papua New Guinea','Australia','Mexico']
    regions = ['Central Africa','Central America','East Africa','East Asia','Europe','North Africa','North America','Northeast Asia','Oceania','South Africa','South America','South Asia','Southeast Asia','Southwest Asia','West Africa','West Indes']

    roundElements = lambda element: round(element)
    vectorize_roundElements = np.vectorize(roundElements)
    rounded_coverage = vectorize_roundElements(data)

    pvals = []
    print(title)
    for population in rounded_coverage:
        pop_zero_no_coverage = 100 - population[0]
        pop_one_no_coverage = 100 - population[1]
        population_ = population.tolist()
        oddsRatio,pvalue = stats.fisher_exact([population_,[pop_zero_no_coverage,pop_one_no_coverage]])
        pvals.append(pvalue)

    if data.shape[0] > 16:
        if comp == 0:
            output = pd.DataFrame(data=data,index=countries,columns=['All PCS','Gag PCS'])
        elif comp == 1:
            output = pd.DataFrame(data=data,index=countries,columns=['All PCS','Pol PCS'])
        else:
            output = pd.DataFrame(data=data,index=countries,columns=['Gag PCS','Pol PCS'])

    else:
        if comp == 0:
            output = pd.DataFrame(data=data,index=regions,columns=['All PCS','Gag PCS'])
        elif comp == 1:
            output = pd.DataFrame(data=data,index=regions,columns=['All PCS','Pol PCS'])
        else:
            output = pd.DataFrame(data=data,index=regions,columns=['Gag PCS','Pol PCS'])


    output['P value'] = pvals
    print(output)
    print('\n')

def anova(title,data):

    # ANOVA to be used exclusively with average hit and pc90 data

    asia = ['Japan','South Korea','Mongolia','China','Hong Kong','Pakistan','India','Sri Lanka','Philippines','Singapore','Malaysia','Thailand','Vietnam','Taiwan','Indonesia','Israel','Oman','Lebanon','UAE','Saudi Arabia','Iran','Jordan']
    africa = ['Kenya','Uganda','Zambia','Zimbabwe','Senegal','Ivory Coast','Burkina Faso','Cape Verde','Guinea Bissau','Sao Tome and Principe','Rwanda','Central African Republic','Cameroon','Morocco','Sudan','Mali','Tunisia','South Africa']
    europe = ['Croatia','England','France','Italy','Spain','Russia','Turkey','Austria','Bulgaria','Czech Republic','Poland','Romania','Scotland','United Kingdom']
    na = ['Cuba','Guatemala','US','Mexico']
    sa = ['Argentina','Brazil','Chile','Ecuador','Peru','Venezuela']
    oceania = ['Papua New Guinea','Australia']

    regions = ['Central Africa','Central America','East Africa','East Asia','Europe','North Africa','North America','Northeast Asia','Oceania','South Africa','South America','South Asia','Southeast Asia','Southwest Asia','West Africa','West Indes']


    all_pcs = []
    gag = []
    pol = []

    print(title)
    for population in data:
        all_pcs.append(population[0])
        gag.append(population[1])
        pol.append(population[2])


    f,pvalue = stats.f_oneway(all_pcs,gag,pol)

    if 'asia' in title:
        output = pd.DataFrame(data=data,index=asia,columns=['All PCS','Gag PCS','Pol PCS'])
    elif 'africa' in title:
        output = pd.DataFrame(data=data,index=africa,columns=['All PCS','Gag PCS','Pol PCS'])
    elif 'europe' in title:
        output = pd.DataFrame(data=data,index=europe,columns=['All PCS','Gag PCS','Pol PCS'])
    elif 'NA' in title:
        output = pd.DataFrame(data=data,index=na,columns=['All PCS','Gag PCS','Pol PCS'])
    elif 'oceania' in title:
        output = pd.DataFrame(data=data,index=oceania,columns=['All PCS','Gag PCS','Pol PCS'])
    elif 'SA' in title:
        output = pd.DataFrame(data=data,index=sa,columns=['All PCS','Gag PCS','Pol PCS'])
    else:
        output = pd.DataFrame(data=data,index=regions,columns=['All PCS','Gag PCS','Pol PCS'])

    output.loc['P value'] = [pvalue,'-','-']
    print(output)
    print('\n')

def crawl(root,folders):

    for folder in folders:
        filenames = os.listdir('{}/{}'.format(root,folder))
        for filename in filenames:
            df_coverage = pd.read_csv('{}/{}/{}'.format(root,folder,filename))
            np_coverage = df_coverage.to_numpy()
            if folder == 'Coverage':
                if 'all' in filename and 'gag' in filename:
                    fisher('Coverage: {}'.format(filename),np_coverage,0)
                elif 'all' in filename and 'pol' in filename:
                    fisher('Coverage: {}'.format(filename),np_coverage,1)
                elif 'gag' in filename and 'pol' in filename:
                    fisher('Coverage: {}'.format(filename),np_coverage,2)
            elif folder == 'Average Hit':
                anova('Average Hit: {}'.format(filename),np_coverage)
            else:
                anova('PC90: {}'.format(filename),np_coverage)




print('DATA BY COUNTRY...')
country_folders = os.listdir('Country')
crawl('Country',country_folders)

print('\n\n\n')
print('DATA BY GEOGRAPHICAL REGION...')
region_folders = os.listdir('Regions')
crawl('Regions',region_folders)
