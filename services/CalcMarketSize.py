import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from tqdm import tqdm


class CalcMarketSize:
    def calc_market_size():
        plt.rcParams['font.sans-serif'] = ['Heiti TC']

        getdata = pd.read_csv('product_info.csv', encoding='utf-8')

        # get tag from description
        containar = []
        for i in range(len(getdata)):
            getArticle = str(getdata['Description'][i])

            getArticle = getArticle.replace('＃', '#')
            item = []
            for j in getArticle.split('#'):
                if len(j) < 10:
                    j = j.replace(' ', '')
                    j = j.replace('^n', '')
                    if len(j) > 0:
                        item.append(j)
            if item and len(item) > 0 and item[0] != 'nan':
                containar.append(item)
            else:
                containar.append('nan')

        getdata['Tag'] = containar
        getdata = getdata[getdata['Tag'] != 'nan']

        KmeansData = getdata[['ItemID', 'Price', 'HistoricalSold', 'Tag']]

        allpro = KmeansData['Tag'].sum()
        allpro = pd.DataFrame(allpro)
        allpro = allpro[allpro[0] != 'nan']

        KmeansData['Tag'] = KmeansData['Tag'].astype(str)
        count = 0
        for i in tqdm(allpro[0].value_counts().index):
            KmeansData['c'+str(count)
                       ] = np.where(KmeansData['Tag'].str.contains(i), 1, 0)
            count = count+1

        crub = 3  # number of clusters
        clf = KMeans(n_clusters=crub)
        clf.fit(KmeansData[['c'+str(x)
                for x in range(count)]].values.tolist())  # start training

        # get result
        getdata['cluster'] = clf.labels_

        # top 20 tags in each cluster
        for i in range(crub):
            draw = getdata[getdata['cluster'] == i]
            draw = pd.DataFrame(draw['Tag'].sum())[0].value_counts()

            plt.bar(draw.index[0: 20],
                    draw[0:20].values,
                    color='#d9f776',
                    alpha=0.5)
            plt.xticks(rotation=70)
            plt.title('cluster' + str(i) + ' top20 tags', fontsize=30)
            plt.xlabel("tag", fontsize=15)
            plt.ylabel("count", fontsize=15)

            plt.tight_layout()
            plt.savefig('cluster' + str(i) + '_top20_tags' + '.png', dpi=300)
            plt.close()

        # gross income in each cluster
        getdata['GrossIncome'] = getdata['Price'] * getdata['HistoricalSold']
        for i in range(crub):
            draw = getdata[getdata['cluster'] == i]
            print('cluster' + str(i) + ' gross income: ' +
                  str(draw['GrossIncome'].sum()))
