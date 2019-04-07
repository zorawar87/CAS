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
    batch_size = 10
    isSingle = False

    def __init__(self, data=None):
        self.rowsProcessed = 0
        if data == None:
            with open("output.json") as jsonSource:
                self.rawJson = json.load(jsonSource)
                #self.documents = { 'documents': json.load(jsonSource) }
        else:
            self.isSingle = True
            self.documents = { 'documents': [{'id':1, 'language':'en', 'text':data }]}

    def postRequest(self, service):
        if self.isSingle:
            return requests.post(self.text_analytics_base_url+service, headers=self.headers, json=self.documents).json()
        else:
            results = []
            while (self.rowsProcessed < self.batch_size):
                print(self.rowsProcessed)
                response  = requests.post(self.text_analytics_base_url+service, headers=self.headers, json=self.prepareDocuments())
                results.push(response.json())
            return results

    def prepareDocuments(self):
        self.documents = { 'documents': self.rawJson[self.rowsProcessed:(self.rowsProcessed+self.batch_size)]}
        self.rowsProcessed += self.batch_size
        return self.documents


    def getLanguage  (self):
        return self.postRequest("languages")

    def getSentiment (self):
        return self.postRequest("sentiment")

    def getKeyPhrases(self):
        return self.postRequest("keyPhrases")

    def show(self):
        print(self.documents)

    def retrieve(self):
        return self.documents

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
