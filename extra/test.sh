curl -H "Content-type: application/json" -X POST \
    -d '{    
      "service_key": "<actually service API token>",
      "incident_key": "srv01/HTTP",
      "event_type": "trigger",
      "description": "FAILURE for production/HTTP on machine srv01.acme.com",
      "client": "Sample Monitoring Service",
      "client_url": "https://monitoring.service.com",
      "details": {
        "ping time": "1500ms",
        "load avg": 0.75
      }
    }' \
    "http://onduty.your.systems/api/create_event"

