import json


class JsonKv(object):
    def format_json(self, batched):
        events = {}
        events["events"] = batched
        return json.dumps(events)

    def format_kv(self, batched):
        aggregated_kv = []
        for event in batched:
            kv_str = ""
            for k, v in event.items():
                kv_str += "%s=\"%s\" " % (k, v)
            kv_str += "\n"
            aggregated_kv.append(kv_str)
        return aggregated_kv