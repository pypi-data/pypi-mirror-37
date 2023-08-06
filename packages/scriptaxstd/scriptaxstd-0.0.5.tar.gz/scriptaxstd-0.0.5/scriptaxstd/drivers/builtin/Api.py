from apitaxcore.builders.HeaderBuilder import HeaderBuilder
from apitaxcore.flow.responses.ApitaxResponse import ApitaxResponse
from commandtax.models.Command import Command
from scriptax.drivers.Driver import Driver
import json


class Api(Driver):
    def isDriverCommandable(self) -> bool:
        return True

    def getDriverName(self) -> str:
        return 'api'

    def getDriverDescription(self) -> str:
        return 'Provides a standard api interface'

    def getDriverHelpEndpoint(self) -> str:
        return 'coming soon'

    def getDriverTips(self) -> str:
        return 'I recommend this website for reading json data: http://json.parser.online.fr/'

    def handleDriverCommand(self, command: Command) -> ApitaxResponse:
        response: ApitaxResponse = ApitaxResponse()

        if '--url' not in command.command:
            return response.res_server_error(body='--url parameter is required for api commands and is not found')

        url = command.command[command.command.index('--url') + 1]
        command.request.preEndpoint = url

        postData = ''  # Post Data
        paramData = ''  # Data container in the URL, but only the part after the ?: someurl.com/user/7?thisIsAParamData=true
        pathData = ''  # Data contained in the URL
        headerData = ''  # Data contained in the headers

        if '--data-post' in command.command:
            postData = command.command[command.command.index('--data-post') + 1]

        if '--data-query' in command.command:
            paramData = command.command[command.command.index('--data-query') + 1]

        if '--data-path' in command.command:
            pathData = command.command[command.command.index('--data-path') + 1]

        if '--data-header' in command.command:
            headerData = command.command[command.command.index('--data-header') + 1]

        if postData != '':
            command.request.bodyBuilder.add(json.loads(str(postData)))

        if paramData != '':
            command.request.queryBuilder.add(json.loads(str(paramData)))

        if pathData != '':
            command.request.path = json.loads(str(pathData))

        if headerData != '':
            command.request.headerBuilder.add(json.loads(str(headerData)))

        command.request.requestFormat = self.getApiFormat()

        if '--get' in command.command:
            command.request.get()
        elif '--post' in command.command:
            command.request.post()
        elif '--put' in command.command:
            command.request.put()
        elif '--patch' in command.command:
            command.request.patch()
        elif '--delete' in command.command:
            command.request.delete()
        else:
            return response.res_server_error(body='No API request method specified')

        return command.request.getResponse()

    def getApiFormat(self) -> str:
        return 'json'

    def getApiStatus(self) -> str:
        return 'up'

    def addApiHeaders(self, headerBuilder: HeaderBuilder) -> HeaderBuilder:
        return headerBuilder.add({'Content-type': 'application/json'})
