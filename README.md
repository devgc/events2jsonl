# events2jsonl
Output Windows Events in JSONL format

## Usage
```
usage: events2jsonl.py [-h] -s SOURCE

events2jsonl.py

Parse Windows Event files and output records in the JSONL format.

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        The source (file or folder)
```

## Output example
Output is line by line json objects. Each line represents an event record.

Record example in pretty print:
```json
{
  "xmlns": "http://schemas.microsoft.com/win/2004/08/events/event",
  "System": {
    "Provider": {
      "Name": "Microsoft-Windows-Security-Auditing",
      "Guid": "{54849625-5478-4994-A5BA-3E3B0328C30D}"
    },
    "EventID": "4945",
    "Version": "0",
    "Level": "0",
    "Task": "13571",
    "Opcode": "0",
    "Keywords": "0x8020000000000000",
    "TimeCreated": {
      "SystemTime": "2013-10-23T02:56:19.463308800Z"
    },
    "EventRecordID": "1774524",
    "Correlation": null,
    "Execution": {
      "ProcessID": "712",
      "ThreadID": "764"
    },
    "Channel": "Security",
    "Computer": "Bifrost",
    "Security": null
  },
  "EventData": {
    "Data": [
      {
        "Name": "ProfileUsed",
        "#text": "Public"
      },
      {
        "Name": "RuleId",
        "#text": "VIRTCL-WMI-ASYNC-In-TCP-NoScope"
      },
      {
        "Name": "RuleName",
        "#text": "Hyper-V Management Clients - WMI (Async-In)"
      }
    ]
  },
  "_source": "C:\\Exports\\Logs\\Security.evtx"
}
```
