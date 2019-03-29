Receive messages from Azure Event Hub. 

Sample system in Sesam Portal:
```json
{
  "_id": "eventhub-system",
  "type": "system:microservice",
  "docker": {
    "environment": {
    ###FILL INN YOUR EVENT HUB CREDENTIALS###
      "ADDRESS": "$ENV(eventhub-address)",
      "CONSUMER_GROUP": "$ENV(eventhub-consumer-group)",
      "KEY": "$SECRET(apikey)",
      "USER": "$ENV(eventhub-usr)"
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
        ["add", "_id", "_S.entityId"],
        ["copy", "*"],
        ["add", "rdf:type",
          ["ni", "input", "pipe"]
        ]
      ]
    }
  }
}
```


