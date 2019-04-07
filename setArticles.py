def setArticles(Scoring, KeyPhrases, Dataset)

        # Scoring is Dict with arg 'scoring'
        # keyPhrases is Dict with arg 'keyPhrases'
        # Dataset is tuple going like this: 
        ### ({id = , score = }, {id = , keyPhrases = })


        import numpy as np
        import pandas as pd


        # User 'input'
        # KeyPhrases['keyPhrases'] = KeyPhrases['keyPhrases'].split(',') # TODO - how will it be deliminated?
        U_I = Scoring['scoring']
        U_I_KP = [KeyPhrases['keyPhrases'].str.len()]

        # Number of keywords with the capital
        x = [str.istitle(y) for y in U_I_KP]
        x = np.sum(x)
        U_I += [x]

        # Relative number of keywords started with capital
        U_I += [U_I[1]/U_I[0]]

        ### Preprocessing
        Dataset = Dataset[0]
        data = pd.DataFrame(index = range(len(Dataset)), columns = ['ID', 'Keywords', 'Sentiment'])
        for k in range(len(Dataset)):
                data.iloc[k,:] = [Dataset[k][0]['id'], Dataset[k][1]['keyPhrases'], Dataset[k][0]['score']]

        #----------------------------#

        # Classify the articles from the database to our post
        # based just on the keywords themselves
        # If 50% of the keywords from the user post will be in the article keywords - add them

        IfIsIn = []
        for k in range(data.shape[0]):
                IfIsIn += [(('Brexit' in (' '.join(data.Keywords))) | ('brexit' in (' '.join(data.Keywords))))]

        #----------------------------#

        from itertools import compress


        data.Keywords = list(compress(Dataset, IfIsIn))

        # Number of keywords
        NrKeywords = []
        for k in range(len(Dataset)):
                NrKeywords = data.Keywords.str.len
        
        data['NrKeywords'] = NrKeywords
        
        # Number of keywords with the capital
        CapKeywords = []
        for i in range(len(Dataset)):
                x = [str.istitle(y) for y in Dataset[i][1]['keyPhrase']]
                x = np.sum(x)
                CapKeywords += [x]

        data['CapKeywords'] = CapKeywords
        data['CapToNrRatio'] = data.CapKeywords/data.NrKeywords

        # # Number of keywords connected to Britain
        # keywords_brit = ['bre', 'bri']

        # BreKeywords = []
        # BriKeywords = []
        # for i in data.Keywords:
        #     for j in keywords_brit:
        #         if j == keywords_brit[0]:
        #             BreKeywords += [sum([(j in x) for x in [str.lower(k) for k in i] ])]
        #         if j == keywords_brit[1]:
        #             BriKeywords += [sum([(j in x) for x in [str.lower(k) for k in i] ])]

        # data['BreKeywords'] = BreKeywords
        # data['BriKeywords'] = BriKeywords


        # # Number of keywords connected to leaving
        # keywords_leave = ['deadlock', 'leave']

        # DeadlockKeywords = []
        # LeaveKeywords = []
        # for i in data.Keywords:
        #     for j in keywords_leave:
        #         if j == keywords_leave[0]:
        #             DeadlockKeywords += [sum([(j in x) for x in [str.lower(k) for k in i] ])]
        #         if j == keywords_leave[1]:
        #             LeaveKeywords += [sum([(j in x) for x in [str.lower(k) for k in i] ])]


        # data['DeadlockKeywords'] = DeadlockKeywords
        # data['LeaveKeywords'] = LeaveKeywords


        #------------------------------------#

        # Does the list have top keywords (from the top 10%)

        # list of all the keywords
        AllKeywords = sum(data.Keywords, [])

        TopKeywords = pd.DataFrame(index = range(len(AllKeywords)), columns = range(2))
        TopKeywords[0] = AllKeywords
        TopKeywords[1] = ([AllKeywords.count(i) for i in AllKeywords])



        # Top Keywords
        TopKeywords = TopKeywords[(TopKeywords[1] >= 5)].drop_duplicates()[0]

        # Are they in our Keywords series?
        TopInData = []
        for i in data.Keywords:
                TopInData += [TopKeywords.isin(i).sum()]

        # Are they in U_I?
        TopInU_I = TopKeywords.isin(KeyPhrases['keyPhrases'])

        # Creating new variables - how many of the TopKeywords does the article have?
        data['Top'] = [x/len(TopKeywords) for x in TopInData]
        U_I += [TopInU_I / len(TopKeywords)]

        # How many TopKeywords does one article have in comparison to all the keywords from that article?
        data['RelTop'] = TopInData/data.NrKeywords
        U_I += [TopInU_I/KeyPhrases['keyPhrases']]

        #------------------------------------#

        # Create Final Pandas

        Final = data[['Sentiment', 'CapKeywords', 'CapToNrRatio', 'Top', 'RelTop']]

        #------------------------------------#

        # Feature Scaling
        from sklearn.preprocessing import StandardScaler, normalize
        sc_X = StandardScaler()
        Final_norm = sc_X.fit_transform(Final)

        #------------------------------------#

        # Clustering

        from sklearn.cluster import KMeans
        n_recommendations = 2

        import math
        NClus = min(3,math.ceil(Final_norm.shape[0] / n_recommendations))
        # Fitting K-Means to the dataset
        kmeans = KMeans(n_clusters = NClus, init = 'k-means++', random_state = 42)
        y_kmeans = kmeans.fit_predict(Final_norm)

        # # Measure the euclidean distances between the points and the centre
        # Distances = pd.DataFrame(index = range(Final_norm.shape[0]), columns = range(kmeans.cluster_centers_.shape[0]))
        # from scipy.spatial import distance
        # for i in range(Final_norm.shape[0]):
        #     for j in range(kmeans.cluster_centers_.shape[0]):
        #         Distances.iloc[i,j] = distance.euclidean(Final_norm[i], kmeans.cluster_centers_[j])

        # ProbPoints = 1 - normalize(Distances, norm='l2')

        # # One-hot encoding the classes
        from sklearn.preprocessing import OneHotEncoder
        onehotencoder = OneHotEncoder(categories='auto')
        y_kmeans_OHE = onehotencoder.fit_transform(y_kmeans.reshape(-1,1)).toarray()
        #------------------------------------#

        ### Classify the User data based on the fit from the train data

        # Transform the data just like test-data was transformed
        User_norm = sc_X.transform(np.array(U_I).reshape(1,-1))
        # Find weights for parameters for the classification (train the model) 
        # CV

        # np.concatenate((Final_norm, (ProbPoints)), axis = 1)

        # from sklearn.model_selection import KFold, cross_val_score

        # k_fold = KFold(n_splits=5)
        # for train_indices, test_indices in k_fold.split(Final_norm):
        #     print('Train: %s | test: %s' % (train_indices, test_indices))

        # Splitting the dataset into the Training set and Test set
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(Final_norm, y_kmeans_OHE, test_size = 0.25, random_state = 0)


        from sklearn import svm
        svc = svm.SVC(C=1, kernel='linear', probability=True)

        # Making the Confusion Matrix
        from sklearn.metrics import confusion_matrix

        # for k in range(NClus):
        #         svc.fit(X_train, y_train[:,k])
        #         y_pred = svc.predict(X_test)
        #         print(confusion_matrix(y_test[:,k], y_pred))

        Pred = pd.DataFrame(index = range(NClus), columns = range(2))

        for k in range(NClus):
                svc.fit(Final_norm, y_kmeans_OHE[:,k])
                # y_pred = svc.predict(User_norm)
                y_pred = svc.predict_proba(User_norm)
                Pred.iloc[k,:] = (y_pred)

        # Pred[0].idxmax()  # NOT WORKING FOR SOME REASON
        Ma = Pred[0].where(Pred[0] == max(Pred[0])).dropna().index
        Mi = Pred[0].where(Pred[0] == min(Pred[0])).dropna().index

        # Output the indecies - worst code I have ever done
        Best = ([i for i, x in enumerate([x == Ma for x in y_kmeans]) if x])
        Worst = ([i for i, x in enumerate([x == Mi for x in y_kmeans]) if x])

        Best = data.loc[Best, :]
        Worst = data.loc[Worst, :]

        return Best.to_json()
        return Worst.to_json()
