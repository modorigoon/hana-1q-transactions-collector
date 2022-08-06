# -*- coding: utf-8 -*-
"""
    Hana 1Q API
    author: modorigoon
    since: 0.1.0
"""
from common.logger import log
from PyQt5.QtCore import *
from PyQt5.QAxContainer import *


class HanaAPI(QAxWidget):

    _real_event_handler = None
    _fid_event_handler = None

    def __init__(self, config):
        """ constructor
        :param config: configuration for API HANDLER
        """
        super().__init__()

        self._PROGRAM_ID = config['program_id']
        self._CREDENTIALS = config['credentials']
        self._REAL_NAME = config['target']['real_name']
        self._SYMBOL = config['target']['symbol']
        self.setControl(self._PROGRAM_ID)

        # self.OnGetFidData.connect(self.fid_data_handler)
        self.OnGetRealData.connect(self.real_data_handler)
        self.OnAgentEventHandler.connect(self.on_agent_event_handler)

        self.event_connect_loop = QEventLoop()

    # -------------------------------------------------------------------------------------------------
    # communication module control part
    # -------------------------------------------------------------------------------------------------

    def comm_init(self) -> bool:
        """ initialize communication module
        :return: initialize successful
        """
        log.info('[api] call - CommInit()')
        result = self.dynamicCall('CommInit()')
        return True if result == 0 else False

    def get_comm_state(self) -> bool:
        """ communication module status inquiry
        :return: normal operation status of communication module
        """
        log.info('[api] call - CommGetConnectState()')
        state = self.dynamicCall('CommGetConnectState()')
        return True if state == 1 else False

    def terminate(self):
        """ terminate communication module
        :return: void
        """
        log.info('[api] call - CommTerminate({})'.format(str(1)))
        self.dynamicCall('CommTerminate(bSocketClose)', 1)

    def get_last_api_error(self):
        """ query the last error message in API
        :return: last error message
        """
        log.info('[api] call - GetLastErrMsg()')
        return self.dynamicCall('GetLastErrMsg()')

    def on_agent_event_handler(self, event_type, param, value):
        """ agent event loop handler
        :param event_type: event type
        :param param: param
        :param value: value
        :return: void
        """
        log.info('[api] on event({}) {} - {}'.format(str(event_type), str(param), str(value)))

    # -------------------------------------------------------------------------------------------------
    # certification part
    # -------------------------------------------------------------------------------------------------

    def set_login_mode(self, option, login_mode):
        """ login mode setting
        :param option: investment and market segmentation
                       0: simulated investments
                       1: only query market price
        :param login_mode:
                       0(option) - 0: real, 1: mock, 2: over seas mock
                       1(option) - 0: cert, 1: only query market price
        :return: setup successful
        """
        log.info('[api] call - SetLoginMode({}, {})'.format(str(option), str(login_mode)))
        result = self.dynamicCall('SetLoginMode(nOption, nMode)', option, login_mode)
        return True if result else False

    def get_login_mode(self, option):
        """ query login mode
        :param option: query option (0: mock, 1: query market price, 2: employee/customer)
        :return: login mode
        """
        log.info('[api] call - GetLoginMode({})'.format(str(option)))
        return self.dynamicCall('GetLoginMode(nOption)', option)

    def login(self) -> bool:
        """ login
        :return: login successful
        """
        try:
            # disable the agent control message dialog
            self.dynamicCall('SetOffAgentMessageBox(nOption)', 1)
            log.info('[api] call - CommLogin(*, *, *)')
            result = self.dynamicCall('CommLogin(sUserId, sPwd, sCertPass)', self._CREDENTIALS['id'],
                                      self._CREDENTIALS['password'], self._CREDENTIALS['cert'])
            return True if result else False
        finally:
            # enable the agent control message dialog
            self.dynamicCall('SetOffAgentMessageBox(nOption)', 0)

    def logout(self) -> bool:
        """ logout
        :return: logout successful
        """
        log.info('[api] call - CommLogout(*)')
        result = self.dynamicCall('CommLogout(sUserId)', self._CREDENTIALS['id'])
        return True if result == 0 else False

    def get_login_state(self) -> bool:
        """ query login state
        :return: login state
        """
        log.info('[api] call - GetLoginState()')
        result = self.dynamicCall('GetLoginState()')
        return True if result else False

    # -------------------------------------------------------------------------------------------------
    # real api part
    # -------------------------------------------------------------------------------------------------

    def register_real(self) -> bool:
        """ subscribe to real register api
        :return: subscribe successful
        """
        log.info('[api] call - RegisterReal({}, {})'.format(str(self._REAL_NAME), str(self._SYMBOL)))
        result = self.dynamicCall('RegisterReal(strRealName, strRealKey)', self._REAL_NAME, self._SYMBOL)
        return True if result == 0 else False

    def unregister_real(self) -> bool:
        """ unsubscribe to real register api
        :return: unsubscribe successful
        """
        try:
            log.info('[api] call - UnRegisterReal({}, {})'.format(str(self._REAL_NAME), str(self._SYMBOL)))
            result = self.dynamicCall('UnRegisterReal(strRealName, strRealKey)', self._REAL_NAME, self._SYMBOL)
            return True if result == 1 else False
        finally:
            if self.event_connect_loop is not None:
                self.event_connect_loop.quit()

    def unregister_real_all(self):
        """ unsubscribe to all register api
        :return: unsubscribe successful
        """
        try:
            log.info('[api] call - AllUnRegisterReal()')
            result = self.dynamicCall('AllUnRegisterReal()')
            return True if result == 1 else False
        finally:
            if self.event_connect_loop is not None:
                self.event_connect_loop.quit()

    def get_real_output_data(self) -> str:
        """ get real api output data
        :return: response data
        """
        log.info('[api] call - GetRealOutputData({}, {})'.format(str(self._REAL_NAME), str(self._SYMBOL)))
        response = self.dynamicCall('GetRealOutputData(strRealName, realItem)', self._REAL_NAME, self._SYMBOL)
        self.event_connect_loop.exec_()
        return response

    def real_data_handler(self, name, key, block, length):
        """ real api event handler
        :param name: real name
        :param key: real key
        :param block: data
        :param length: length of data
        :return: void
        """
        log.debug('[api] receive real: {}'.format(str(block)))
        self._real_event_handler(block)

    def set_real_event_handler(self, event_handler):
        """ set real event handler
        :param event_handler: handler
        :return: void
        """
        self._real_event_handler = event_handler

    # -------------------------------------------------------------------------------------------------
    # FID event part
    # -------------------------------------------------------------------------------------------------

    def fid_data_handler(self, rid, block, length):
        """ FID api handler
        :param rid: request id
        :param block: data block
        :param length: length of data
        :return: void
        """
        # below is an example of the processing reference logic, not actual business logic.
        count = self.get_fid_output_count(rid)
        log.debug('[api] received data count: {}'.format(str(count)))
        responses = []
        for i in range(0, count):
            response = {'TIME': self.get_fid_output_data(rid, '8', i), 'DATE': self.get_fid_output_data(rid, '9', i)}
            responses.append(response)
        log.debug('[api] response output: {}'.format(str(responses)))

    def create_request_id(self):
        """ generate inquiry id all request ids are required for FID inquiry
        :return: request id
        """
        log.info('[api] call - CreateRequestID()')
        return self.dynamicCall('CreateRequestID()')

    def release_request_id(self, rid):
        """ release request id
        :param rid: request id
        :return: void
        """
        log.info('[api] call - ReleaseRqId({})'.format(str(rid)))
        self.dynamicCall('ReleaseRqId(nRqId)', rid)

    def set_fid_input(self, rid, fid, value):
        """ FID inquiry input value registration
        :param rid: request id
        :param fid: FID
        :param value: input value
        :return: register input value successful
        """
        log.info('[api] call - SetFidInputData({}, {}, {})'.format(str(rid), str(fid), str(value)))
        result = self.dynamicCall('SetFidInputData(nRqId, strFID, strValue)', rid, fid, value)
        return True if result == 1 else False

    def request_fid(self, rid, fields, screen_no):
        """ request fid (single record)
        :param rid: request id
        :param fields: search result fields
        :param screen_no: screen number
        :return: FID number
        """
        log.info('[api] call - RequestFid({}, {}, {})'.format(str(rid), str(fields), str(screen_no)))
        return self.dynamicCall('RequestFid(nRqId, strOutputFidList, strScreenNo)', rid, fields, screen_no)

    def request_fid_data_list(self, rid, fields, pn, pnc, screen_no, req_count):
        """ request fid (multiple records)
        :param rid: request id
        :param fields: search result fields
        :param pn: classification of continuous queries (0: normal, 1: FOC, 2: BOC, 3: next)
        :param pnc: serial transaction key received in response to inquiry
        :param screen_no: screen number
        :param req_count: number of data to receive in response to inquiry (max: 9999)
        :return: FID number
        """
        log.info('[api] call - RequestFidArray({}, {}, {}, {}, {}, {})'.format(str(rid), str(fields), str(pn), str(pnc),
                                                                               str(screen_no), str(req_count)))
        fid_code = self.dynamicCall('RequestFidArray(nRqId, strOutputFidList, strPreNext, strPreNextContext, '
                                    'strScreenNo, nRequestCount)', rid, fields, pn, pnc, screen_no, req_count)
        self.event_connect_loop.exec_()
        return fid_code

    def get_fid_output_count(self, rid):
        """ FID count of data inquiry response data
        :param rid: request id
        :return: count of data
        """
        log.info('[api] call - GetFidOutputRowCnt({})'.format(str(rid)))
        return self.dynamicCall('GetFidOutputRowCnt(nRequestId)', rid)

    def get_fid_output_data(self, rid, fid, row):
        """ FID return data inquiry response value
        :param rid: count of response data
        :param fid: response field FID value
        :param row: data row INDEX
        :return: response data
        """
        log.info('[api] call - GetFidOutputData({}, {}, {})'.format(str(rid), str(fid), str(row)))
        return self.dynamicCall('GetFidOutputData(nRequestId, strFid, nRow)', rid, fid, row)
