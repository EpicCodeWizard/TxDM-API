from flask import Flask, request, jsonify
from alwaysOnline import AlwaysOnline
from corsHelper import fix_cors
from pyairtable import Table
import os

app = Flask(__name__)
AlwaysOnline(app)
table = Table(os.environ["AIRTABLE_KEY"], "appMB6P1AlDkbfsnf", "Tissue Sample")

def getDataByID(id):
  data = table.get(id)["fields"]
  try:
    del data["id"]
  except:
    pass
  finally:
    try:
      del data["Created By"]
    except:
      pass
    finally:
      try:
        del data["Last Modified"]
      except:
        pass
      finally:
        try:
          del data["Last Modified By"]
        except:
          pass
        finally:
          try:
            del data["Last Modified 2"]
          except:
            pass
          finally:
            return data

def getTable(expandTags=False):
  retdata = {}
  maxkeys = []
  for record in table.all():
    data = record["fields"]
    if expandTags:
      try:
        del data["id"]
      except:
        pass
      finally:
        try:
          del data["Created By"]
        except:
          pass
        finally:
          try:
            del data["Last Modified"]
          except:
            pass
          finally:
            try:
              del data["Last Modified By"]
            except:
              pass
            finally:
              try:
                del data["Last Modified 2"]
              except:
                pass
              finally:
                pass
      recids = data.get("Machine / Assay Specs", None)
      if recids:
        for index, recid in enumerate(recids):
          data["Machine / Assay Specs"][index] = getDataByID(recid)["Name"]
    retdata[data.pop("Tissue")] = data
    maxkeys += list(data.keys())
  maxkeys = list(tuple(maxkeys))
  maxkeys = {k: None for k in maxkeys}
  maxkeys["Machine / Assay Specs"] = []
  maxkeys["Cancer"] = False
  maxkeys["Rare Disease"] = False
  maxkeys["FFPE"] = False
  for k, record in retdata.items():
    for key, value in maxkeys.items():
      try:
        record[key]
        if record["FFPE"] == "FFPE":
          retdata[k]["FFPE"] = True
      except:
        retdata[k][key] = value
  return retdata

@app.route("/latest", methods=["GET"])
@fix_cors
def latest():
  healthData = getTable()
  cancerTissues = []
  rareDiseaseTissues = []
  for k, v in healthData.items():
    if v["Cancer"]:
      cancerTissues.append(k)
    if v["Rare Disease"]:
      rareDiseaseTissues.append(k)
  return jsonify({"cancer": cancerTissues, "rare_disease": rareDiseaseTissues})

@app.route("/submit", methods=["POST"])
@fix_cors
def testing():
  healthData = getTable(expandTags=True)
  userData = request.json
  return jsonify(healthData)

app.run(host="0.0.0.0")