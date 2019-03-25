Receive messages from Azure Event Hub. 

Sample system in Sesam Portal:
```json
{
  "_id": "eventhub-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
    ###FILL INN YOUR EVENT HUB CREDENTIALS###
      "ADDRESS": "$ENV(gcp-address)",
      "CONSUMER_GROUP": "$ENV(gcp-consumer-group)",
      "KEY": "$SECRET(apikey)",
      "USER": "$ENV(gcp-usr)"
    },
    "image": "<dockerhub_username>/<repoistory>:<tag>",
    "port": 5000
  },
  "verify_ssl": true
}
```

Sample input pipe:
```json
{
  "_id": "input-pipe",
  "type": "pipe",
  "source": {
    "type": "json",
    "system": "eventhub-system",
    "is_chronological": true,
    "supports_since": true,
    "url": "/"
  },
  "transform": {
    "type": "dtl",
    "rules": {
      "default": [
        ["add", "_id", "_S.meteringPointId"],
        ["copy", "*"],
        ["add", "rdf:type",
          ["ni", "input", "pipe"]
        ]
      ]
    }
  }
}
```


