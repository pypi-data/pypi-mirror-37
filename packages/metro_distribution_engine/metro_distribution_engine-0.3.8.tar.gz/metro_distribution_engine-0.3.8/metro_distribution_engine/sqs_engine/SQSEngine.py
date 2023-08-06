import boto3
import logging
import json
import os
import requests
import types

logging.getLogger('botocore').setLevel(logging.ERROR)

logging.basicConfig(level=os.environ.get("LOGLEVEL", "DEBUG"),
                    format='%(asctime)s - %(name)s - %(levelname)s:\t %(message)s')

from metro_distribution_engine.BaseEngine import BaseEngine

class SQSEngine(BaseEngine):
    def __init__(self, debug):
        super().__init__()
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        self.sns_client = boto3.client('sns',
                aws_access_key_id=os.environ['METRO_AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['METRO_AWS_SECRET_KEY'])
        self.sqs_client = boto3.client('sqs',
                aws_access_key_id=os.environ['METRO_AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['METRO_AWS_SECRET_KEY'])
        self.s3_client = boto3.client('s3',
                aws_access_key_id=os.environ['METRO_AWS_ACCESS_KEY'],
                aws_secret_access_key=os.environ['METRO_AWS_SECRET_KEY'])

        self.AWS_ID = os.environ['AWS_ID']

        self._sns_extension = "_sns-topic"

        self._sqs_prefix = "metro-data_"
        self._sqs_extension = "_sqs-queue"

        self._s3_extension = ".zip"

        self._internal_endpoint = "https://getmetro.co"
        self._mtr_internal_key = os.environ['MTR_INTERNAL_KEY']

    def __getattribute__(self, attr):
        '''
        This runs before an attribute (variable or method) is accessed.

        We check if the attribute is a method and whether or not dev mode is turned on.
        If both are true, we log a dummy log and return an empty function to be executed instead
        of the 'real' function.
        '''
        attribute = object.__getattribute__(self, attr)
        debug = object.__getattribute__(self, 'debug')
        if attribute is None:
            raise Exception("Method %s not implemented" % attr)
        if type(attribute) == types.MethodType and debug: # Debug mode is turned on and we're planning to execute a function
            self.logger.debug(f"Dummy call for {attribute.__name__} since dev_mode is turned on")
        return attribute

                #########################
                ### Private Functions ###
                #########################

    def _generate_queue_name(self, project_slug, ds_slug):
        return f"{self._sqs_prefix}{project_slug}_{ds_slug}{self._sqs_extension}"

    def _generate_topic_name(self, datasource_name):
        return datasource_name + self._sns_extension

    def _create_topic(self, topic_name):
        '''Create an SNS topic with the given name and returns its ARN.'''
        topic_atts = self.sns_client.create_topic(Name=topic_name)

        return topic_atts['TopicArn']

    def _create_queue(self, queue_name):
        '''Create an SQS queue with the given name.'''
        queue_url = self.sqs_client.create_queue(QueueName=queue_name)['QueueUrl']
        queue_details = self.sqs_client.get_queue_attributes(QueueUrl=queue_url,
                AttributeNames=['QueueArn'])

        self.logger.info("Created queue %s: " % queue_name)
        self.logger.info(queue_details)

        # We need the URL to add a permission to the queue and the ARN to subscribe
        # it to the SNS topic -_-
        return queue_url, queue_details['Attributes']['QueueArn']

    def _subscribe_queue_to_topic(self, queue_arn, topic_arn):
        '''Subscribes a queue_arn to a topic_arn and returns the
        SubscriptionARN.'''
        return self.sns_client.subscribe(TopicArn=topic_arn, Protocol='sqs',
                Endpoint=queue_arn)['SubscriptionArn']

    def _update_queue_policy(self, queue_arn, queue_url, topic_arn):
        '''Updates the queue policy to allow receiving from a list of topic
        arns.'''

        # Create the queue policy holder.
        queue_policy = {
                "Statement": [
                    {
                        "Effect": "Allow",
                        "Principal": {"AWS": "*"},
                        "Action": "SQS:SendMessage",
                        "Resource": queue_arn,
                        "Condition": {
                            "ArnLike": {
                                "aws:SourceArn": topic_arn
                                }
                            }
                        }
                    ]
                }

        self.sqs_client.set_queue_attributes(QueueUrl=queue_url,
                Attributes={"Policy": json.dumps(queue_policy)})

    def _update_filter_policy(self, queue_arn, project_name):
        '''Updates the subscription_arn's filter policy to only receive
    messages passed with an AttributeName of project_name.'''
        self.sns_client.set_subscription_attributes(
                SubscriptionArn=queue_arn,
                AttributeName = 'FilterPolicy',
                AttributeValue = '{"' + project_name + '": ["true"]}'
                )

    def _get_metrics_batch(self, metro_subscription):
        '''Returns and deletes up to 10 messages from the queue.'''
        queue_url = metro_subscription['queue_url']

        # I'm sure there's nicer ways to do this...
        # Read message until we get one... Stupid SQS doesn't guarantee
        # receiving a response.
        # Python has no do .. while():
        response = self.sqs_client.receive_message(
                QueueUrl = queue_url,
                # 10 is the max number of messages retreivable at a time.
                MaxNumberOfMessages = 10
                )
        # Retry up to 5 times:
        for i in range(5):
            try:
                if len(response['Messages']) == 0:
                    # No messsages left.
                    return None
                else:
                    # Got messages
                    break
            except Exception as e:
                if i == 4:
                    return None

                # Or just retry:
                response = self.sqs_client.receive_message(
                        QueueUrl = queue_url,
                        MaxNumberOfMessages = 10
                        )

        # As SQS was clearly designed by the gods themselves, you have to
        # manually delete a message:
        messages = []
        for message in response['Messages']:
            receipt_handle = message['ReceiptHandle']
            self.sqs_client.delete_message(
                    QueueUrl = queue_url,
                    ReceiptHandle = receipt_handle
                    )
            messages.append(json.loads(message['Body'])['Message'])

        return messages

    def _get_s3_key_from_slugs(self, project_slug, datasource_slug):
        '''Given slugs, return the s3 zip file name.'''
        return f"{project_slug}_{datasource_slug}{self._s3_extension}"

    def _init_empty_s3_zip(self, s3_key):
        '''Given an S3 key, put an empty zip file in its place.'''
        # See https://stackoverflow.com/questions/25195495/how-to-create-an-empty-zip-file

        empty_zip_data = b'PK\x05\x06\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

        self.s3_client.put_object(
                Bucket = 'metro-data-for-download',
                Key = s3_key,
                Body = empty_zip_data
        )

        return

    def _add_dataprofiles(self, messages, project):
        '''
        Given a dict of metrics, add the dataprofile data to each message and
        return it as a dict.
        '''
        new_messages = []

        for message in messages:
            message = json.loads(message)
            query_url = self._internal_endpoint + "/internal/api/dataprofile/data/"
            current_user = message['user']

            payload = {
                    'mtr-internal-key': self._mtr_internal_key,
                    'project-slug': project,
                    'username': current_user
                    }

            r = requests.post(query_url, data=payload)
            if r.status_code == requests.codes.ok:
                response = r.json()
                if response['status'] == 1:
                    message['profile'] = {}

                    for key in response['content']:
                        message['profile'][key] = response['content'][key]
            new_messages.append(message)
            
        return new_messages


        ########################
        ### Engine Functions ###
        ########################

    def create_datasource(self, datasource):
        '''
        When a datasource is created, we create an SNS Topic which distriutes its metrics
        :param datasource:
        :return topic_arn:
        '''
        if self.debug:
            return "debug_arn"

        topic_name = self._generate_topic_name(datasource['slug'])
        topic_arn = self._create_topic(topic_name)
        self.logger.info("Created topic '%s' for datasource named '%s'" % (topic_name, datasource['name']))

        return topic_arn

    def attach(self, project, datasource):
        '''
        When a buyer adds a datasource to a project, we create an SQS Queue which connects
        the two together.
        :param project:
        :param datasource:
        :return queue_url, queue_arn, topic_arn:
        '''
        if self.debug:
            return "https://queue.url", "debug_queue_arn", "debug_topic_arn"

        queue_name = self._generate_queue_name(project['slug'], datasource['slug']) # Generate a name for the queue
        queue_url, queue_arn = self._create_queue(queue_name)

        topic_arn = datasource['topic_arn']

        subscription_arn = self._subscribe_queue_to_topic(queue_arn, topic_arn)
        self.logger.info("Queue %s subscribed to topic %s" % (queue_arn, topic_arn))
        self._update_queue_policy(queue_arn, queue_url, topic_arn)
        self.logger.info("Queue (arn: %s, url: %s) policy updated for new subscription")
        self._update_filter_policy(subscription_arn, project['slug'])
        self.logger.info("Queue (arn: %s, url: %s) filter updated for project slug %s" % (queue_arn,
            queue_url,
            project['slug']))

        # Create the S3 bucket too:
        s3_key = self._get_s3_key_from_slugs(project['slug'], datasource['slug'])
        self._init_empty_s3_zip(s3_key)
        self.logger.info(f"Created the S3 object {s3_key}")

        return queue_url, queue_arn, topic_arn

    def detach(self, metro_subscription):
        '''
        When a buyer removes a datasource from a project, we remove the connection between
        SNS Topic and SQS Queue
        :param metro_subscription:
        :return:
        '''
        if self.debug:
            return

        # First assert that the queue is empty - don't want to delete other
        # than that:
        queue_attributes = self.sqs_client.get_queue_attributes(QueueUrl=metro_subscription['queue_url'], AttributeNames=['ApproximateNumberOfMessages'])
        message_count = queue_attributes['Attributes']['ApproximateNumberOfMessages']
        if(int(message_count) > 0):
            raise Exception("Queue still contains messages.")

        # Overwrite the Policies for the SQS Queue:
        self.sqs_client.delete_queue(
                QueueUrl=metro_subscription['queue_url']
                )

        # Finally, unsubscribe using the SubscriptionArn:
        response = self.sns_client.list_subscriptions_by_topic(TopicArn=metro_subscription['topic_arn'])
        for subscription in response['Subscriptions']:
            if subscription['Endpoint'] == metro_subscription['queue_arn']:
                self.sns_client.unsubscribe(SubscriptionArn=
                        subscription['SubscriptionArn'])
                break

        # Destroy the S3 bucket too:
        s3_key = self._get_s3_key_from_slugs(metro_subscription['project_slug'],
                metro_subscription['ds_slug'])

        self.s3_client.delete_object(
                Bucket = 'metro-data-for-download',
                Key = s3_key
        )
        self.logger.info(f"Deleted the S3 object {s3_key}")

    def send_metric(self, datasource_name, project_names, metric):
        '''Publishes a message to an SNS topic so it will be received by all of
        the project_names specified.'''
        if self.debug:
            return

        # First get the topic ARN:
        topic_name = self._generate_topic_name(datasource_name)
        topic_arn = self._create_topic(topic_name)

        # Then create the message attributes to allow all project names
        # specified to receive the message:
        attributes = {}
        for project_name in project_names:
            attributes[project_name] = {
                    'DataType': 'String',
                    'StringValue': 'true'
                    }

            # Finally publish the message:
        self.sns_client.publish(
                TopicArn = topic_arn,
                Message = metric,
                MessageAttributes = attributes
                )

    def get_metrics(self, metro_subscription):
        '''Returns and deletes all messages from the queue.'''
        if self.debug:
            data = ['{ "a": "a", "user": "admin" }']

            data = self._add_dataprofiles(data, metro_subscription['project_slug'])
            return json.dumps(data)

        messages = []

        # Hard limit on 10k messages for the moment.
        while(len(messages) < 10000):
            # If there are no more messages in the queue, break:
            queue_attributes = self.sqs_client.get_queue_attributes(
                    QueueUrl=metro_subscription['queue_url'],
                    AttributeNames=['ApproximateNumberOfMessages'])
            message_count = queue_attributes['Attributes']['ApproximateNumberOfMessages']

            if(int(message_count) == 0):
                break
            else:
                new_batch = self._get_metrics_batch(metro_subscription)
                if(new_batch is not None):
                    messages.extend(new_batch)

        messages = self._add_dataprofiles(messages,
                metro_subscription['project_slug'])
        return json.dumps(messages)

    def get_datapoints_pending_count(self, metro_subscription):
        '''
        Returns the number of datapoints which are available for collection in the subscription
        :param metro_subscription:
        :return ApproximateNumberOfMessages:
        '''
        if self.debug:
            return 5

        queue_attributes = self.sqs_client.get_queue_attributes(
            QueueUrl=metro_subscription['queue_url'],
            AttributeNames=['ApproximateNumberOfMessages'])

        return queue_attributes['Attributes']['ApproximateNumberOfMessages']
