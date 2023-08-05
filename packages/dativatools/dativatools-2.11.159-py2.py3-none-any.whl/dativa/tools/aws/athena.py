# (c) 2012-2018 Dativa, all rights reserved
# -----------------------------------------
#  This code is licensed under MIT license (see license.txt for details)
import boto3
import logging
import time
import os
from .task_queue import TaskQueue
from dativa.tools.pandas import CSVHandler
from dativa.tools.aws import S3Location

logger = logging.getLogger("dativa.tools.aws")


class Object(object):
    pass


class AthenaClientError(Exception):
    """
    A generic class for reporting errors in the athena client
    """

    def __init__(self, reason):
        Exception.__init__(self, 'Athena Client failed: reason {}'.format(reason))
        self.reason = reason


class AthenaClient(TaskQueue):
    """
    A client for AWS Athena that will create tables from S3 buckets (using AWS Glue)
    and run queries against these tables.
    """

    def __init__(self, region, db, max_queries=3, max_retries=3, s3_parquet=None):
        """
        Create an AthenaClient

        ## Parameters

        region - the AWS region to create the object, e.g. us-east-2
        db - the Glue database to use
        max_queries - the maximum number of queries to run at any one time, defaults to three
        max_retries - the maximum number of times execution of the query will be retried on failure

        """
        self.athena = boto3.client(service_name='athena', region_name=region)
        self.glue = boto3.client(service_name='glue', region_name=region,
                                 endpoint_url='https://glue.{0}.amazonaws.com'.format(region))
        self.db_name = db
        self.aws_region = region
        self.scp = s3_parquet

        super(AthenaClient, self).__init__(max_queries, max_retries)

    def _update_task_status(self, task):
        """
        Gets the status of the query, and updates its status in the queue.
        Any queries that fail are reset to pending so they will be run a second time
        """

        logger.debug("...checking status of query {0}".format(task.name))
        status = self.athena.get_query_execution(QueryExecutionId=task.id)["QueryExecution"]["Status"]

        if status["State"] == "RUNNING":
            task.is_complete = False
        elif status["State"] == "SUCCEEDED":
            task.is_complete = True
            if task.arguments["parquet"]:
                logger.info("starting conversion to")
                self.scp.convert("{0}{1}.csv".format(task.arguments["output_location"],
                                                     task.id),
                                 delete_csv=True,
                                 name="convert {0}".format(task.name))
        else:
            if "StateChangeReason" in status:
                task.error = status["StateChangeReason"]
            else:
                task.error = status["State"]

    def _trigger_task(self, task):
        """
        Runs a query in Athena
        """

        logger.info("Starting query {0} to {1}".format(task.name, task.arguments["output_location"]))

        task.id = self.athena.start_query_execution(
            QueryString=task.arguments["sql"],
            QueryExecutionContext={'Database': self.db_name},
            ResultConfiguration={'OutputLocation': task.arguments["output_location"]}
        )["QueryExecutionId"]

    def add_query(self, sql, name, output_location, parquet=False):
        """
        Adds a query to Athena. Respects the maximum number of queries specified when the module was created.
        Retries queries when they fail so only use when you are sure your syntax is correct!
        Returns a query object

        ## Parameters

        - sql - the SQL query to run
        - name - the name which will be logged when running this query
        - location - the S3 prefix where you want the results stored

        """
        loc = S3Location(output_location)

        if parquet is True and self.scp is None:
            raise AthenaClientError("Cannot output in Parquet without a S3Csv2Parquet object")

        query = self.add_task(name=name,
                              args={"sql": sql,
                                    "output_location": loc.s3_url,
                                    "parquet": parquet})

        return query

    def wait_for_completion(self):
        """Wait cor completion of any queries and also any pending parquet conversions
        :rtype: object
        """
        super(AthenaClient, self).wait_for_completion()
        if self.scp is not None:
            self.scp.wait_for_completion()

    def _db_exists(self):
        for database in self.glue.get_databases(MaxResults=1000)["DatabaseList"]:
            if database["Name"] == self.db_name:
                return True
        return False

    def csv_to_table(self,
                    s3_target,
                    exclusions=None,
                    columns=None,
                    timestamp_formats="yyyy-MM-dd HH:mm:ss,yyyy-MM-dd'T'HH:mm:ss'Z',yyyy-MM-dd'T'HH:mm:ss",
                    header_lines=1,
                    schema_change_policy=None,
                    aws_role='AWSGlueServiceRoleDefault',
                    ):

        loc = S3Location(s3_target)

        return self.create_table(crawler_target={'S3Targets': [
            {'Path': loc.s3_url,
             'Exclusions': exclusions if type(exclusions) is list else [exclusions]}]},
            table_name=loc.prefix.split("/")[-1].replace("-", "_"),
            columns=columns,
            schema_change_policy=schema_change_policy,
            aws_role=aws_role,
            serde='org.apache.hadoop.hive.serde2.OpenCSVSerde',
            serde_parameters={"skip.header.line.count": "{0}".format(header_lines),
                                    'timestamp.formats': timestamp_formats})

        """
        Should we do it like this?
        
        CREATE EXTERNAL TABLE IF NOT EXISTS panels (
                     luid string,
                     device_id string,
                     weight float,
                     scaling_factor float
                )
                PARTITIONED BY (
                  panel_name string)
                ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
                WITH SERDEPROPERTIES ('skip.header.line.count' = '1')
                LOCATION '{path}'
                
        """

    def create_table(self,
                     crawler_target,
                     table_name,
                     columns=None,
                     schema_change_policy=None,
                     aws_role='AWSGlueServiceRoleDefault',
                     serde=None,
                     serde_parameters=None):
        """
        Creates a table in AWS Glue using a crawler.

        ## Parameters

        - region: the AWS region in which to create the table
        - db_name: the name of the Glue database in which to create the table
        - crawler_target: the definition of where the crawler should crawl

        Optional parameters
        - columns: column definitions, typically required for CSV
        - schema_change_policy: the schema change policy to use
        - aws_role: the role that Glue should use when creating it
        - serde: the SerDe to use when parsing the files on S3
        - serde_parameters: any parameters to pass to the SerDe

        For more information on the crawler target and the schema change policies, go here:
        https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-crawler-crawling.html

        Columns are defined here:
        https://docs.aws.amazon.com/glue/latest/dg/aws-glue-api-catalog-tables.html

        """

        if schema_change_policy is None:
            schema_change_policy = {'UpdateBehavior': 'UPDATE_IN_DATABASE', 'DeleteBehavior': 'DEPRECATE_IN_DATABASE'}

        if serde_parameters is None:
            serde_parameters = []

        crawler_name = "{1}_{0}_crawler".format(self.db_name, table_name)

        # creare the database if it exists
        if not self._db_exists():
            self.glue.create_database(DatabaseInput={"Name": self.db_name})

        # if the crawler exists then update it:
        have_updated = False
        for crawler in self.glue.get_crawlers(MaxResults=1000)["Crawlers"]:
            if crawler_name == crawler["Name"]:
                logger.info("updating crawler {0}".format(crawler_name))
                self.glue.update_crawler(Name=crawler_name,
                                         Role=aws_role,
                                         Targets=crawler_target,
                                         DatabaseName=self.db_name,
                                         Classifiers=[],
                                         SchemaChangePolicy=schema_change_policy)
                have_updated = True
                break

        # otherwise create it
        if not have_updated:
            logger.info("creating crawler {0} ".format(crawler_name))
            self.glue.create_crawler(Name=crawler_name,
                                     Role=aws_role,
                                     Targets=crawler_target,
                                     DatabaseName=self.db_name,
                                     Classifiers=[],
                                     SchemaChangePolicy=schema_change_policy)

        # start the crawler and wait for it to complete:
        logger.info("starting crawler {0}".format(crawler_name))
        self.glue.start_crawler(Name=crawler_name)
        while self.glue.get_crawler(Name=crawler_name)["Crawler"]["State"] != "READY":
            logger.info("... waiting for crawler {0} to finish".format(crawler_name))
            time.sleep(5)

        if columns is not None or serde is not None:
            # get the table and update the column names
            logger.info("updating tables {0}".format(table_name))
            table = self.glue.get_table(DatabaseName=self.db_name, Name=table_name)["Table"]

            if columns is not None:
                table["StorageDescriptor"]["Columns"] = columns

            if serde is not None:
                table["StorageDescriptor"]["SerdeInfo"]["SerializationLibrary"] = serde

            if "Parameters" in table["StorageDescriptor"]["SerdeInfo"]:
                for key in serde_parameters:
                    table["StorageDescriptor"]["SerdeInfo"]["Parameters"][key] = serde_parameters[key]
            else:
                table["StorageDescriptor"]["SerdeInfo"]["Parameters"] = serde_parameters

            self.glue.update_table(DatabaseName=self.db_name,
                                   TableInput={'Name': table_name,
                                               'StorageDescriptor': table["StorageDescriptor"],
                                               'PartitionKeys': table["PartitionKeys"],
                                               'TableType': table["TableType"],
                                               'Parameters': table["Parameters"]})

            # now check for partitions
            partitions = self.glue.get_partitions(DatabaseName=self.db_name, TableName=table_name)

            for partition in partitions["Partitions"]:
                logger.info("Updating partition {0}".format(partition["Values"]))
                if columns is not None:
                    partition["StorageDescriptor"]["Columns"] = columns

                if serde is not None:
                    partition["StorageDescriptor"]["SerdeInfo"]["SerializationLibrary"] = serde

                if "Parameters" in partition["StorageDescriptor"]["SerdeInfo"]:
                    for key in serde_parameters:
                        partition["StorageDescriptor"]["SerdeInfo"]["Parameters"][key] = serde_parameters[key]
                else:
                    partition["StorageDescriptor"]["SerdeInfo"]["Parameters"] = serde_parameters

                self.glue.update_partition(DatabaseName=self.db_name,
                                           TableName=table_name,
                                           PartitionValueList=partition["Values"],
                                           PartitionInput={'StorageDescriptor': partition["StorageDescriptor"],
                                                           'Values': partition["Values"]})
        # delete the crawler...
        self.glue.delete_crawler(Name=crawler_name)

    def get_query_result(self, query):
        """
        Returns Pandas DataFrame containing query result if query has completed
        """
        self._update_task_status(query)

        if query.is_complete:
            if query.error:
                raise AthenaClientError("Cannot fetch results since query failed")
            else:
                filepath = os.path.join(query.arguments["output_location"], "{}.csv".format(query.id))
                logger.info("Fetching results from {}".format(filepath))
                csv = CSVHandler()
                df = csv.load_df(filepath)
                return df
        else:
            raise AthenaClientError("Cannot fetch results since query hasn't completed")
