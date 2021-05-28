import json
measurements = []
response = {'measurements': [28761930]}
target_probe_id = 123456

measurements.append(response['measurements'][0])

measurements.append(target_probe_id)
filename = "measurements/test.json"
with open(filename, 'w') as outfile:
    json.dump(measurements, outfile)