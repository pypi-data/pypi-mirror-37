from slackclient import SlackClient
from swimlane import Swimlane
from swimlane.core.search import EQ, NOT_EQ, CONTAINS, EXCLUDES, GT, GTE, LT, LTE
import json
import os


class Setup:
    def __init__(self, sw_config, sw_inputs, sw_user=None):
        for k, v in sw_inputs.iteritems():
            setattr(self, k, v)
        for k, v in sw_config.iteritems():
            setattr(self, k, v)
        #for k, v in sw_user.iteritems():
        #   setattr(self, k, v)

    def mergeTwoDicts(self, x, y):
        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z


class Records(Setup):
    def __init__(self, config_file, sw_config, sw_inputs, proxySet=False, slackNotify=False):
        Setup.__init__(self, sw_config, sw_inputs)
        self.config = json.loads(config_file)
        self.app = None
        self.appRaw = None
        self.crossApp = None
        self.crossAppId = None
        self.crossAppRaw = None
        self.crossRecordId = None
        self.proxySet = proxySet
        if self.proxySet:
            os.environ['HTTPS_PROXY'] = self.proxyUrl
        self.recordData = None
        self.recordKeys = []
        self.records = None
        self.recordsFieldOnly = {}
        self.report = None
        self.slackApiResults = {}
        self.slackNotify = slackNotify
        if self.slackNotify:
            self.sc = SlackClient(self.slackToken)
        self.swimlane = Swimlane(self.swimlaneApiHost, self.swimlaneApiUser, self.swimlaneApiKey, verify_ssl=False)
        self.sw_config = sw_config
        self.sw_inputs = sw_inputs

    def getApp(self, crossAppId=None):
        if crossAppId is not None:
            self.crossAppId = crossAppId
            self.app = self.swimlane.apps.get(id=self.crossAppId)
        else:
            self.app = self.swimlane.apps.get(id=self.ApplicationId)

    def getAppRaw(self, crossAppId=None):
        if crossAppId is not None:
            self.crossAppId = crossAppId
            self.app = self.swimlane.apps.get(id=self.crossAppId)
        else:
            self.app = self.swimlane.apps.get(id=self.ApplicationId)
        self.appRaw = self.app._raw

    def getRecord(self, crossAppId=None, crossRecordId=None):
        if crossAppId is not None and crossRecordId is not None:
            self.getApp(crossAppId)
            self.crossRecordId = crossRecordId
            self.records = self.app.records.get(id=self.crossRecordId)
        else:
            self.getApp()
            self.records = self.app.records.get(id=self.RecordId)

    def getRecordKeys(self, records):
        keys = []
        for r in records:
            keys.append(r[0])
        self.recordKeys = keys

    def getReport(self, reportName, filters=None, crossAppId=None, limit=50):
        if crossAppId is not None:
            self.getApp(crossAppId)
        else:
            self.getApp()
        self.report = self.app.reports.build(reportName, limit=limit)
        if filters is not None:
            for f in filters:
                self.report.filter(f[0], f[1], f[2])

    def pullFieldsFromRecords(self, crossAppId=None, crossRecordId=None, fields=None):
        if crossAppId is not None and crossRecordId is not None:
            self.getRecord(crossAppId, crossRecordId)
        else:
            self.getRecord()
        self.getRecordKeys(self.records)
        if fields:
            oldFields = self.records
            newFields = {}
            for f in fields:
                if f in self.recordKeys:
                    newFields[f] = oldFields[f]
            self.recordsFieldOnly = newFields
            return self.recordsFieldOnly
        else:
            return self.records

    def buildSwOutputs(self, integrationId,  includedFields, staticFields=None):
        self.pullFieldsFromRecords(includedFields)
        if staticFields:
            self.recordData = self.mergeTwoDicts(self.mergeTwoDicts(self.mergeTwoDicts(self.sw_config, self.sw_inputs), self.recordsFieldOnly), staticFields)
        else:
            self.recordData = self.mergeTwoDicts(self.mergeTwoDicts(self.sw_config, self.sw_inputs), self.recordsFieldOnly)
        if self.slackNotify:
            self.sendSlackMessage(self.formatSlackMessage(integrationId))
        return self. recordData

    def formatSlackMessage(self, integrationId):
        if self.slackNotify:
            return self.config['Slack'][integrationId].format(self.config['SwimlaneUrl'], self.ApplicationId, self.RecordId)

    def sendSlackMessage(self, message):
        if self.slackNotify:
            self.setSlackChannel()
            slackChannel = self.recordData['Slack Channel']
            if self.recordData['Slack TS'] is not None:
                threadTs = self.recordData['Slack TS']
                self.slackApiResults = self.sc.api_call("chat.postMessage", channel=slackChannel, text=message, thread_ts=threadTs)
            else:
                self.slackApiResults = self.sc.api_call("chat.postMessage", channel=slackChannel, text=message)
                self.recordData['Slack TS'] = self.slackApiResults['message']['ts']

    def setSlackChannel(self):
        if self.slackNotify:
            slackChannel = self.recordData["Slack Channel"]
            if slackChannel is None:
                self.recordData["Slack Channel"] = self.config['Slack']['primaryChannel']