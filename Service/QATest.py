import urllib3
import json


def getQuery(accessKey, question, passage):
    openApiURL = "http://aiopen.etri.re.kr:8000/MRCServlet"
    requestJson = {
    "access_key": accessKey,
    "argument": {
        "question": question,
        "passage": passage
    }
    }

    http = urllib3.PoolManager()
    response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
    )
    #print(str(response.data, 'utf-8'))
    return str(response.data, 'utf-8')
