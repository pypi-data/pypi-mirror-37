from dynamodb_json import json_util as dynamodb_util


class DynamoStreamEventHandler:
    """
    This handler reads the stream event and figures out what has changed.
    """
    @staticmethod
    def is_dynamo_stream_event(event):
        """
        Determines if the incoming event is a DynamoDB stream event.
        :param event: The incoming event
        :return: `True` if the event has records. `False` otherwise.
        """
        return "Records" in event

    def __init__(self, event):
        self.records = event.get("Records", [])

    def get_changed_record_information(self):
        """
        Returns a list of details about what has changed with the incoming records.
        :return: A dictionary with the modified and deleted records in the following shape:
        ```
        {
            "modifications": [ # delta records ],
            "deletions": [ # deletion records ],
        }
        ```

        For "modifications", it is a list of deltas.  Each delta is structured in the following way:
        ```
        {
            "value": { # The changed value in normalized JSON },
            "modified_columns": [ # The list of attributes that were changed on this record ]
            "source_table_name": # The name of the table this value came from
        }
        ```

        * The `value` is a normalized JSON and NOT in the DynamoDB JSON format.
        * The `modified_columns` includes columns that were removed, added, or whose value was modified.
        * The `source_table_name`, for Properly, includes the environment of the table.

        For "deletions", it is a list of deletions.  Each deletion is structured in the following way:
        ```
        {
            "value": { # The original value in normalized JSON },
            "modified_columns": [ # The list of attributes that were changed on this record. That is, all the columns. ]
            "source_table_name": # The name of the table this value came from
        }
        ```

        * The `value` is a normalized JSON and NOT in the DynamoDB JSON format.
        * The `modified_columns` includes all the columns that were deleted.
        * The `source_table_name`, for Properly, excludes the environment of the table.

        """
        record_deltas = []
        record_deletions = []
        for record in self.records:
            event_name = record.get("eventName")
            if event_name == "REMOVE":
                # Record was removed. Create a deletion record.
                record_deletion = self._get_record_deletion(record)
                record_deletions.append(record_deletion)
            else:
                record_delta = self._get_record_delta(record)
                record_deltas.append(record_delta)

        return {
            "modifications": record_deltas,
            "deletions": record_deletions,
        }

    def _get_record_delta(self, record):
        """
        Calculates the delta for a single DynamoDB record
        :param record: A single DynamoDB record
        :return: A dictionary representing the delta.  The delta is structured in the following way:
        ```
        {
            "value": { # The changed value in normalized JSON },
            "modified_columns": [ # The list of attributes that were changed on this record ]
            "source_table_name": # The name of the table this value came from
        }
        ```

        * The `value` is a normalized JSON and NOT in the DynamoDB JSON format.
        * The `modified_columns` includes columns that were removed, added, or whose value was modified.
        * The `source_table_name`, for Properly, excludes the environment of the table.
        """
        diff_record = record.get("dynamodb")
        new_record = diff_record.get("NewImage")
        event_name = record.get("eventName")
        modified_columns = list(new_record.keys())
        if event_name == "MODIFY":
            # Make this output consistent for unit testing purposes
            modified_columns = sorted(list(self._get_modified_columns_set(record)))

        return {
            "value": self._get_new_value(record),
            "modified_columns": modified_columns,
            "source_table_name": self._get_table_name(record),
        }

    def _get_record_deletion(self, record):
        """
        Calculates the deletion for a single DynamoDB record
        :param record: A single DynamoDB record
        :return: A dictionary representing the deletion.  The deletion is structured in the following way:
        ```
        {
            "value": { # The deleted value in normalized JSON },
            "modified_columns": [ # The list of attributes that were changed on this record. That is, all the columns. ]
            "source_table_name": # The name of the table this value came from
        }
        ```

        * The `value` is a normalized JSON and NOT in the DynamoDB JSON format.
        * The `modified_columns` includes all the columns that were deleted.
        * The `source_table_name`, for Properly, excludes the environment of the table.
        """
        diff_record = record.get("dynamodb")
        old_record = diff_record.get("OldImage")
        modified_columns = list(old_record.keys())

        return {
            "value": self._get_old_value(record),
            "modified_columns": modified_columns,
            "source_table_name": self._get_table_name(record),
        }

    def _get_old_value(self, record):
        """
        Returns the normalized JSON for the *old* value. This is *not* in DynamoDB JSON format.
        :param record: A single DynamoDB record
        :return: The new record in normalized JSON.
        """
        return self._get_image_by_key(record, "OldImage")

    def _get_new_value(self, record):
        """
        Returns the normalized JSON for the *new* value. This is *not* in DynamoDB JSON format.
        :param record: A single DynamoDB record
        :return: The new record in normalized JSON.
        """
        return self._get_image_by_key(record, "NewImage")

    @staticmethod
    def _get_image_by_key(record, image_key):
        """
        Returns the record based on the image key.
        :param record: A single DynamoDB record
        :param image_key: The new record in normalized JSON.
        :return:
        """
        diff_record = record.get("dynamodb")
        new_record = diff_record.get(image_key)
        json_record = dynamodb_util.loads(new_record)
        return json_record

    @staticmethod
    def _get_modified_columns_set(record):
        """
        Calculates which columns have been removed, added, or modified.
        :param record: A single DynamoDB record
        :return: A list of column names that have changed.
        """
        diff_record = record.get("dynamodb")
        new_record = diff_record.get("NewImage")
        old_record = diff_record.get("OldImage", {})

        changed_key_set = set([])
        for key in new_record:
            if key not in old_record:
                # This column is in the new record, but not the old record
                # Therefore, this column was added to the record
                changed_key_set.add(key)

            if new_record.get(key) != old_record.get(key):
                # The column exists in both records, but changed
                # Therefore, this column was modified
                changed_key_set.add(key)

        for key in old_record:
            # Go through the old record columns
            # If a column exists in the old record, but not in the new record
            # Therefore, the column was removed from the record
            # Note: We do not need to capture changed values because it was captured above
            if key not in new_record:
                changed_key_set.add(key)

        return changed_key_set

    @staticmethod
    def _get_table_name(record):
        """
        The source ARN is in the format of:
        'arn:aws:dynamodb:us-east-1:529943178829:table/staging-listing-clean-001/stream/2018-10-18T19:46:17.718'

        We are doing the following:
        * looking for the first backslash '/' and second backslash '/'
        * then parsing out the environment out of the string

        :param record: The DynamoDB stream record
        :return: The environment agnostic table name
        """

        source_arn = record.get("eventSourceARN")

        first_index = source_arn.index("/", 0)
        second_index = source_arn.index("/", first_index+1)
        full_table_name = source_arn[first_index+1:second_index]

        first_dash_index = full_table_name.index("-", 0)
        simplified_table_name = full_table_name[first_dash_index+1:]
        return simplified_table_name
