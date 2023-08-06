import json

__author__ = 'Yaisel Hurtado <hurta2yaisel@gmail.com>'
__date__ = '15/06/18'


class Event(object):
    """

    """

    def __init__(self):
        """

        """
        self.TimeStamp = None
        self.EventDescription = None
        self.Dimensions = {}
        self.Properties = {}
        self.EventType = "APIRequest"

    @property
    def event_type(self):
        """

        :return:
        """
        return self.EventType

    def to_json(self):
        """

        :return:
        """
        return json.dumps(self.__dict__)


class DependencyEvent(Event):
    """

    """

    def __init__(self, dependency_name, dependency_duration):
        """

        :param dependency_name:
        :param dependency_duration:
        """
        super(DependencyEvent, self).__init__()
        self.Properties.update({
            "DependencyName": dependency_name,
            "DependencyDuration": dependency_duration,
        })
        self.EventType = "Dependency"

    @property
    def dependency_name(self):
        """

        :return:
        """
        if "DependencyName" in self.Dimensions:
            return str(self.Properties.get('DependencyName', ''))
        return ''

    @dependency_name.setter
    def dependency_name(self, value):
        """

        :param value:
        :return:
        """
        self.Properties["DependencyName"] = str(value)

    @property
    def dependency_duration(self):
        """

        :return:
        """
        if "DependencyDuration" in self.Dimensions:
            return int(str(self.Properties.get('DependencyDuration', -1)))
        return -1

    @dependency_duration.setter
    def dependency_duration(self, value):
        """

        :param value:
        :return:
        """
        self.Properties["DependencyDuration"] = int(value)


class ExceptionEvent(Event):
    """

    """

    def __init__(self, exception_message, exception_type, exception_stack_trace, **properties):
        """

        :param exception_message:
        :param exception_type:
        :param exception_stack_trace:
        :param properties:
        """
        super(ExceptionEvent, self).__init__()
        self.Properties.update({
            "ExceptionMessage": exception_message,
            "ExceptionType": exception_type,
            "ExceptionStackTrace": exception_stack_trace
        })
        self.Properties.update(properties)
        self.EventType = "Exception"

    @property
    def exception_message(self):
        """

        :return:
        """
        if "ExceptionMessage" in self.Dimensions:
            return str(self.Properties.get('ExceptionMessage', ''))
        return ''

    @exception_message.setter
    def exception_message(self, value):
        """

        :param value:
        :return:
        """
        self.Properties["ExceptionMessage"] = str(value)

    @property
    def exception_type(self):
        """

        :return:
        """
        if "ExceptionType" in self.Dimensions:
            return int(str(self.Properties.get('ExceptionType', '')))
        return ''

    @exception_type.setter
    def exception_type(self, value):
        """

        :param value:
        :return:
        """
        self.Properties["ExceptionType"] = str(value)

    @property
    def exception_stack_trace(self):
        """

        :return:
        """
        if "ExceptionStackTrace" in self.Dimensions:
            return int(str(self.Properties.get('ExceptionStackTrace', '')))
        return ''

    @exception_stack_trace.setter
    def exception_stack_trace(self, value):
        """

        :param value:
        :return:
        """
        self.Properties["ExceptionStackTrace"] = str(value)
