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

    def __init__(self):
        with open("converted.json") as jsonSource:
            self.documents = { 'documents': json.load(jsonSource) }

    def postRequest(self, service):
        print(service)
        response  = requests.post(self.text_analytics_base_url+service, headers=self.headers, json=self.documents)
        pprint(response.json())

    def getLanguage  (self):
        self.postRequest("languages")

    def getSentiment (self):
        self.postRequest("sentiment")

    def getKeyPhrases(self):
        self.postRequest("keyPhrases")

    def show(self):
        print(self.documents)

TextAnalyser().getKeyPhrases()
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
