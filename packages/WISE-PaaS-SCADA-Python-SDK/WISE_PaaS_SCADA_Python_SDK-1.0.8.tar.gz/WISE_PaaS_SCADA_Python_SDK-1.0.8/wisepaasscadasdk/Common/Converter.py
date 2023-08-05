from wisepaasscadasdk.Model.MQTTMessage import *
import wisepaasscadasdk.Common.Constants as constant
from wisepaasscadasdk.Model.Edge import *

def convertData(data = None):
  try:
    if data is None:
      return (False, None)
    payloads = []
    count = 0
    dataMessage = None
    tagList = data.tagList
    tagList = sorted(tagList, key = lambda tag: tag.deviceId)

    for tag in tagList:
      if dataMessage is None:
        dataMessage = DataMessage()
      dataMessage.setTagValue(tag.deviceId, tag.tagName, tag.value)
      count += 1
      if count == constant.DataMaxTagCount:
        payloads.append(dataMessage.getJson())
        dataMessage = None
    payloads.append(dataMessage.getJson())
    return (True, payloads)
  except Exception as error:
    print('convert data fail', str(error))
    return (False, None)
    

def convertDeviceStatus(status = None):
  try:
    if not status:
      return (False, None)
    deviceList = status.deviceList
    payload = DeviceStatusMessage()
    for device in deviceList:
      payload.setDeviceStatus(device.id, device.status)
    return (True, payload.getJson())
  except Exception as error:
    print('convert status fail', str(error))
    return (False, None)

def convertCreateorUpdateConfig(action = None, scadaId = None, config = None, heartbeat = constant.HeartbeatInterval):
  try:
    if not config or not scadaId:
      return (False, None)
    payload = ConfigMessage(action, scadaId)

    scada = config.scada
    if not type(scada) is ScadaConfig:
      raise ValueError('config.scada type is invalid')
    scada.heartbeat = heartbeat
    (result, error) = scada.isValid()
    if action == constant.ActionType['Create'] and not result:
      raise error
    payload.addScadaConfig(scadaId, scada)
    for device in scada.deviceList:
      if not type(device) is DeviceConfig:
        raise ValueError('config.scada.device type is invalid')
      (result, error) = device.isValid()
      if action == constant.ActionType['Create'] and not result:
        raise error
      payload.addDeviceConfig(scadaId, deviceId = device.id, config = device)
      for tag in device.analogTagList:
        tag.type = constant.TagType['Analog']
        payload.addTagConfig(scadaId, deviceId = device.id, tagName = tag.name, config = tag)
      for tag in device.discreteTagList:
        tag.type = constant.TagType['Discrete']
        payload.addTagConfig(scadaId, deviceId = device.id, tagName = tag.name, config = tag)
      for tag in device.textTagList:
        tag.type = constant.TagType['Text']
        payload.addTagConfig(scadaId, deviceId = device.id, tagName = tag.name, config = tag)
    return (True, payload.getJson())
  except Exception as error:
    print('convert create config fail', str(error))
    return (False, None)

def convertDeleteConfig(action = None, scadaId = None, config = None):
  try:
    if not (config or scadaId):
      return (False, None)
    payload = ConfigMessage(action, scadaId)

    scada = config.scada
    if not type(scada) is ScadaConfig:
      raise ValueError('config.scada type is invalid')
    payload.deleteScadaConfig(scadaId)
    for device in scada.deviceList:
      payload.deleteDeviceConfig(scadaId, deviceId = device.id)
      for listName in ['analogTagList', 'discreteTagList', 'textTagList']:
        for tag in getattr(device, listName):
          payload.deleteDeviceConfig(scadaId, deviceId = device.id)
        for tag in device.analogTagList:
          payload.deleteTagConfig(scadaId, deviceId = device.id, tagName = tag.name)
        for tag in device.discreteTagList:
          payload.deleteTagConfig(scadaId, deviceId = device.id, tagName = tag.name)
        for tag in device.textTagList:
          payload.deleteTagConfig(scadaId, deviceId = device.id, tagName = tag.name)
    return (True, payload.getJson())
  except Exception as error:
    print('convert create config fail', str(error))
    return (False, None)
