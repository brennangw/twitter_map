prototypeSettings = {
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    },
    "mappings": {
        "urls": {
            "properties": {
                "url": {
                    "type": "string"
                },
                "location": {
                    "type": "geo_point"
                }
            }
        },

     }
}