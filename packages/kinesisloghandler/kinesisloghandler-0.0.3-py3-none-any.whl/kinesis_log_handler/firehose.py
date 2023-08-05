import logging
import platform
import json
import boto3


class FirehoseHandler(logging.Handler):
    """
    Firehose logging handler.
    """
    def __init__(self, delivery_stream_name, region_name,
                 aws_access_key_id=None, aws_secret_access_key=None,
                 log_level=logging.INFO):
        """
        Use FirehoseJSONFormatter as the default logging formatter
        """
        super(FirehoseHandler, self).__init__(level=log_level)
        self.setFormatter(FirehoseJSONFormatter())
        self._delivery_stream_name = delivery_stream_name
        self._log_service_name = 'firehose'
        self._client = self.get_client(
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    def get_client(self, region_name,
                   aws_access_key_id, aws_secret_access_key):
        """
        Get AWS service client.
        """
        return boto3.client(
            self._log_service_name, region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key)

    def get_firehose_record(self, record):
        """
        Get firehose formatted log record.
        """
        return {
            'Data': self.format(record),
        }

    def emit(self, record):
        """
        Emit log recort to aws firehose client
        """
        try:
            self._client.put_record(
                DeliveryStreamName=self._delivery_stream_name,
                Record=self.get_firehose_record(record)
            )
        except Exception:  # pragma: no cover
            self.handleError(record)


class FirehoseJSONFormatter(logging.Formatter):
    """
    Default JSON record formatter.
    """
    def __init__(self, ensure_ascii=False):
        self._platform_dict = dict(platform.uname()._asdict())
        self._ensure_ascii = ensure_ascii

    def jsonify(self, log_record):
        return json.dumps(log_record, ensure_ascii=self._ensure_ascii)+'\n'

    def format(self, record):
        data = {}
        for key, value in record.__dict__.items():
            if key == 'exc_info' and value is not None:
                value = self.formatException(value)
            else:
                data[key] = value
        # Add platform info
        data.update({'platform': self._platform_dict})
        return self.jsonify(data)
