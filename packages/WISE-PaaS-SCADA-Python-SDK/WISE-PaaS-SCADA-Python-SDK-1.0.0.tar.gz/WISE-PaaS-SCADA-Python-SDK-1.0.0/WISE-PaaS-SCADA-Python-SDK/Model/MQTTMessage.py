import json
import datetime
import WISEPaaS-SCADA-Python-SDK.Common.Constants as constant

format = '%Y-%m-%dT%H:%M:%S%z'

class Message(dict):
  def __init__(self):
    self.message = {}
    self.message['d'] = {}
    self.message['ts'] = datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
  def __repr__(self):
    return repr(self.__dict__)
  def getJson(self):
    return json.dumps(self.message)

class LastWillMessage(Message):
  def __init__(self):
    super().__init__()
    self.message['d'] = {
      'UeD': 1
    }  

class DisconnectMessage(Message):
  def __init__(self):
    super().__init__()
    self.message['d'] = {
      'DsC': 1
    }

class HeartbeatMessage(Message):
  def __init__(self):
    super().__init__()
    self.message['d'] = {
      'Hbt': 1
    }
    
class ConnectMessage(Message):
  def __init__(self):
    super().__init__()
    self.message['d'] = {
      'Con': 1
    }

class DataMessage(Message):
  def __init__(self):
    super().__init__()

  def setTagValue(self, deviceId, tagName, value):
    if not (deviceId in self.message['d']):
      self.message['d'][deviceId] = {}
    self.message['d'][deviceId][tagName] = value

class DeviceStatusMessage(Message):
  def __init__(self):
    super().__init__()
    self.message['d'] = {
      'Dev': {}
    }
  
  def setDeviceStatus(self, deviceId, status):
    self.message['d']['Dev'][deviceId] = status

class ConfigMessage(Message):
  def __init__(self, action = None, scadaId = None):
    super().__init__()
    if not action in constant.ActionType.values():
      raise ValueError('action is invalid')
    if scadaId is None or scadaId == '':
      raise ValueError('action is necessary')
    self.message['d'] = {
      'Action': action,
      'Scada': {}
    }
    self.message['d']['Scada'][scadaId] = {}
  
  def addScadaConfig(self, scadaId, config):
    _config = {}
    mapper = constant.ScadaConfigMapper
    for key in mapper:
      value = getattr(config, key, None)
      if not value is None:
        _config[mapper[key]] = value
    self.message['d']['Scada'][scadaId] = _config

  def deleteScadaConfig(self, scadaId):
    self.message['d']['Scada'][scadaId] = {}
  
  def addDeviceConfig(self, scadaId, deviceId, config):
    _config = {}
    mapper = constant.DeviceConfigMapper
    for key in mapper:
      value = getattr(config, key, None)
      if not value is None:
        _config[mapper[key]] = value

    if not scadaId in self.message['d']['Scada']:
      self.message['d']['Scada'][scadaId] = {}
    if not 'Device' in self.message['d']['Scada'][scadaId]:
      self.message['d']['Scada'][scadaId]['Device'] = {}
    self.message['d']['Scada'][scadaId]['Device'][deviceId] = _config
  
  def deleteDeviceConfig(self, scadaId, deviceId):
    if not scadaId in self.message['d']['Scada']:
      self.message['d']['Scada'][scadaId] = {}
    if not 'Device' in self.message['d']['Scada'][scadaId]:
      self.message['d']['Scada'][scadaId]['Device'] = {}
    self.message['d']['Scada'][scadaId]['Device'][deviceId] = {}

  def addTagConfig(self, scadaId, deviceId, tagName, config):
    _config = {}
    mapper = constant.TagConfigMapper
    boolMapper = ['readOnly']
    for key in mapper:
      value = getattr(config, key, None)
      if not value is None:
        if key in boolMapper:
          value = 1 if value == True else 0
        _config[mapper[key]] = value

    if not scadaId in self.message['d']['Scada']:
      self.message['d']['Scada'][scadaId] = {}
    if not 'Device' in self.message['d']['Scada'][scadaId]:
      self.message['d']['Scada'][scadaId]['Device'] = {}
    if not deviceId in self.message['d']['Scada'][scadaId]['Device']:
      self.message['d']['Scada'][scadaId]['Device'][deviceId] = {}
    if not 'Tag' in self.message['d']['Scada'][scadaId]['Device'][deviceId]:
      self.message['d']['Scada'][scadaId]['Device'][deviceId]['Tag'] = {}
    self.message['d']['Scada'][scadaId]['Device'][deviceId]['Tag'][tagName] = _config

  def deleteTagConfig(self, scadaId, deviceId, tagName):
    if not scadaId in self.message['d']['Scada']:
      self.message['d']['Scada'][scadaId] = {}
    if not 'Device' in self.message['d']['Scada'][scadaId]:
      self.message['d']['Scada'][scadaId]['Device'] = {}
    if not deviceId in self.message['d']['Scada'][scadaId]['Device']:
      self.message['d']['Scada'][scadaId]['Device'][deviceId] = {}
    if not 'Tag' in self.message['d']['Scada'][scadaId]['Device'][deviceId]:
      self.message['d']['Scada'][scadaId]['Device'][deviceId]['Tag'] = {}
    self.message['d']['Scada'][scadaId]['Device'][deviceId]['Tag'][tagName] = {}

