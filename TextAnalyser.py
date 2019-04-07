import requests
import json
from pprint import pprint

class TextAnalyser:
    text_analytics_base_url = "https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/"
    subscription_key = "959d5505253946f49743d1ea0a9858a1"
    headers   = {
                    "Ocp-Apim-Subscription-Key": subscription_key,
                    "Content-Type": "application/json",
                    "Accept":"application/json"
                }
    #batch_size = 1800
    batch_size = 8
    isSingle = False

    def __init__(self, data=None):
        self.rowsProcessed = 0
        if data == None:
            with open("output.json") as jsonSource:
                self.rawJson = json.load(jsonSource)
                #self.documents = { 'documents': json.load(jsonSource) }
        else:
            self.isSingle = True
            self.documents = {'documents': [{'id':1, 'language':'en', 'text': data}]}

    def postRequest(self, service):
        if self.isSingle:
            return requests.post(self.text_analytics_base_url+service, headers=self.headers, json=self.documents).json()
        else:
            results = []
            #while (self.rowsProcessed < len(self.rawJson) and self.rowsProcessed < self.rowsProcessed + self.batch_size):
            while (self.rowsProcessed < self.batch_size*5 and self.rowsProcessed < self.rowsProcessed + self.batch_size):
                print(self.rowsProcessed)
                response  = requests.post(self.text_analytics_base_url+service, headers=self.headers, json=self.prepareDocuments())
                results.append(response.json())
                self.rowsProcessed += self.batch_size
            return results

    def prepareDocuments(self):
        subarray = self.rawJson[self.rowsProcessed:(self.rowsProcessed+self.batch_size)]
        for article in subarray:
            article["text"] = article["text"][0:5000]
        self.documents = {'documents': subarray}
        return self.documents

    def mergeBatches(self, batches):
        singular =[]
        for batch in batches:
            singular.extend(batch["documents"])
        return singular

    def mergeWithSource(self, results):
        for result in results:
            for score in result["documents"]:
                try:
                    score.update(self.rawJson[int(score["id"])])
                except ValueError:
                    print("error with ")
                    pprint(score)
        return results

    def getLanguage  (self):
        self.rowsProcessed = 0
        return self.postRequest("languages")

    def getSentiment (self):
        self.rowsProcessed = 0
        if self.isSingle:
            return self.postRequest("sentiment")
        else:
            return self.mergeBatches(self.postRequest("sentiment"))

    def getKeyPhrases(self):
        self.rowsProcessed = 0
        if self.isSingle:
            return self.postRequest("keyPhrases")
        else:
            return self.mergeBatches(self.postRequest("keyPhrases"))

    def getKeyInfo(self):
        s = self.getSentiment()
        k = self.getKeyPhrases()
        s["documents"][0].update(k["documents"][0])
        return s["documents"][0] 

    def show(self):
        print(self.documents)

    def retrieve(self):
        return self.documents

    def interleave(self):
        dataset = []
        sentiments = self.getSentiment()
        phrases = self.getKeyPhrases()
        dataset.extend(zip(sentiments, phrases))
        return dataset

    def write(self, dataset):
        with open("dataset.json",'w') as ds:
            json.dump(dataset, ds)

t = TextAnalyser()

"""
TextAnalyser({ 
    'documents': [ 
            { 'id': '1',
               'text': 'This is a document written in English.' 
           }, { 'id': '2',
              'text': 'Este es un document escrito en Español.' 
           }, { 'id': '3',
               'text': '这是一个用中文写的文件' } 
   ]
}).getLanguage()

TextAnalyser({ 
    'documents': [ 
            { 'id': '1',
               'text': 'This is a document written in English.',
           }, { 'id': '2',
               'text': 'Este es un document escrito en Español.',
           }, { 'id': '3',
               'text': '这是一个用中文写的文件',
               } 
   ]
}).getSentiment()

getSentiment({
    'documents' : [
          {'id': '1',
          'language': 'en',
          'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'
          }, {'id': '2',
              'language': 'en',
              'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'
          }, {'id': '3',
              'language': 'es',
              'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'
          }, {'id': '4',
              'language': 'es',
              'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]})

getKeyPhrases({
    'documents' : [
          {'id': '1',
          'language': 'en',
          'text': 'I had a wonderful experience! The rooms were wonderful and the staff was helpful.'
          }, {'id': '2',
              'language': 'en',
              'text': 'I had a terrible time at the hotel. The staff was rude and the food was awful.'
          }, {'id': '3',
              'language': 'es',
              'text': 'Los caminos que llevan hasta Monte Rainier son espectaculares y hermosos.'
          }, {'id': '4',
              'language': 'es',
              'text': 'La carretera estaba atascada. Había mucho tráfico el día de ayer.'}
]})
"""
