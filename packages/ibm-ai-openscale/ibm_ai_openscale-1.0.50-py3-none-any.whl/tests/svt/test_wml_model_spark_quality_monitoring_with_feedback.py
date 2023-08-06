import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from models_preparation import *
from preparation_and_cleaning import *


class TestAIOpenScaleClient(unittest.TestCase):
    deployment_uid = None
    model_uid = None
    aios_model_uid = None
    scoring_url = None
    labels = None
    logger = logging.getLogger(__name__)
    ai_client = None
    wml_client = None
    subscription = None
    test_uid = str(uuid.uuid4())

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()
        self.spark_credentials = get_spark_reference()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_model(self):
        from pyspark.ml.feature import OneHotEncoder, StringIndexer, IndexToString, VectorAssembler
        from pyspark.ml.classification import DecisionTreeClassifier
        from pyspark.ml.evaluation import MulticlassClassificationEvaluator
        from pyspark.ml import Pipeline, Model

        from pyspark import SparkContext, SQLContext
        ctx = SparkContext.getOrCreate()
        sc = SQLContext(ctx)

        db2_service_credentials = {
          "port": 50000,
          "db": "BLUDB",
          "username": "dash13173",
          "ssljdbcurl": "jdbc:db2://dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net:50001/BLUDB:sslConnection=true;",
          "host": "dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net",
          "https_url": "https://dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net:8443",
          "dsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50000;PROTOCOL=TCPIP;UID=dash13173;PWD=UDoy3w_qT9W_;",
          "hostname": "dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net",
          "jdbcurl": "jdbc:db2://dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net:50000/BLUDB",
          "ssldsn": "DATABASE=BLUDB;HOSTNAME=dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net;PORT=50001;PROTOCOL=TCPIP;UID=dash13173;PWD=UDoy3w_qT9W_;Security=SSL;",
          "uri": "db2://dash13173:UDoy3w_qT9W_@dashdb-entry-yp-lon02-01.services.eu-gb.bluemix.net:50000/BLUDB",
          "password": "UDoy3w_qT9W_"
        }
        spark_credentials = get_spark_reference()
        train_data = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ";").option("inferSchema", "true").load(os.path.join(os.curdir, 'datasets', 'drugs', 'drug_feedback_data.csv'))
        test_data = sc.read.format("com.databricks.spark.csv").option("header", "true").option("delimiter", ";").option("inferSchema", "true").load(os.path.join(os.curdir, 'datasets', 'drugs', 'drug_feedback_test.csv'))

        stringIndexer_sex = StringIndexer(inputCol='SEX', outputCol='SEX_IX')
        stringIndexer_bp = StringIndexer(inputCol='BP', outputCol='BP_IX')
        stringIndexer_chol = StringIndexer(inputCol='CHOLESTEROL', outputCol='CHOL_IX')
        stringIndexer_label = StringIndexer(inputCol="DRUG", outputCol="label").fit(train_data)

        vectorAssembler_features = VectorAssembler(inputCols=["AGE", "SEX_IX", "BP_IX", "CHOL_IX", "NA", "K"], outputCol="features")
        dt = DecisionTreeClassifier(labelCol="label", featuresCol="features")
        labelConverter = IndexToString(inputCol="prediction", outputCol="predictedLabel", labels=stringIndexer_label.labels)
        pipeline_dt = Pipeline(stages=[stringIndexer_label, stringIndexer_sex, stringIndexer_bp, stringIndexer_chol, vectorAssembler_features, dt, labelConverter])

        model = pipeline_dt.fit(train_data)
        predictions = model.transform(test_data)
        evaluatorDT = MulticlassClassificationEvaluator(labelCol="label", predictionCol="prediction", metricName="accuracy")
        accuracy = evaluatorDT.evaluate(predictions)

        training_data_reference = {
            "name": "DRUG feedback",
            "connection": db2_service_credentials,
            "source": {
                "tablename": "DRUG_TRAIN_DATA_UPDATED",
                "type": "dashdb"
            }
        }

        model_props = {
            TestAIOpenScaleClient.wml_client.repository.ModelMetaNames.NAME: "Best Heart Drug Selection",
            TestAIOpenScaleClient.wml_client.repository.ModelMetaNames.TRAINING_DATA_REFERENCE: training_data_reference,
            TestAIOpenScaleClient.wml_client.repository.ModelMetaNames.EVALUATION_METHOD: "multiclass",
            TestAIOpenScaleClient.wml_client.repository.ModelMetaNames.EVALUATION_METRICS: [
                {
                    "name": "accuracy",
                    "value": 0.7,
                    "threshold": 0.8
                }
            ]
        }

        published_model_details = TestAIOpenScaleClient.wml_client.repository.store_model(model=model, meta_props=model_props, training_data=train_data, pipeline=pipeline_dt)
        TestAIOpenScaleClient.model_uid = TestAIOpenScaleClient.wml_client.repository.get_model_uid(published_model_details)

        deployment = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.enable(evaluation_method='multiclass', threshold=0.8, min_records=5, spark_credentials=self.spark_credentials)

    def test_09_get_quality_monitoring_details(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.get_details()

    def test_10_send_feedback_data(self):
        TestAIOpenScaleClient.subscription.feedback_logging.store(
            [
                [74.0, 'M', 'HIGH', 'HIGH', 0.715337, 0.074773, 'drugB'],
                [58.0, 'F', 'HIGH', 'NORMAL', 0.868924, 0.061023, 'drugB'],
                [68.0, 'F', 'HIGH', 'NORMAL', 0.77541, 0.0761, 'drugB'],
                [65.0, 'M', 'HIGH', 'NORMAL', 0.635551, 0.056043, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB'],
                [60.0, 'F', 'HIGH', 'HIGH', 0.800607, 0.060181, 'drugB'],
                [70.0, 'M', 'HIGH', 'HIGH', 0.658606, 0.047153, 'drugB'],
                [60.0, 'M', 'HIGH', 'HIGH', 0.805651, 0.057821, 'drugB'],
                [59.0, 'M', 'HIGH', 'HIGH', 0.816356, 0.058583, 'drugB']
            ],
            fields=['AGE', 'SEX', 'BP', 'CHOLESTEROL', 'NA', 'K', 'DRUG']
        )

    def test_10b_run_learning_iteration(self):
        run_details = TestAIOpenScaleClient.wml_client.learning_system.run(TestAIOpenScaleClient.model_uid, asynchronous=False)
        print(run_details)
        import time
        time.sleep(20)
        self.assertTrue(run_details['entity']['status']['state'] == 'COMPLETED')
        TestAIOpenScaleClient.wml_client.learning_system.list_metrics(TestAIOpenScaleClient.model_uid)

    def test_11_stats_on_quality_monitoring_table(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.print_table_schema()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.show_table(limit=None)
        TestAIOpenScaleClient.subscription.quality_monitoring.describe_table()
        TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content()
        quality_metrics = TestAIOpenScaleClient.subscription.quality_monitoring.get_table_content(format='python')
        self.assertTrue(len(quality_metrics['values']) > 0)

    def test_11b_stats_on_feedback_logging_table(self):
        TestAIOpenScaleClient.subscription.feedback_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.feedback_logging.show_table()
        TestAIOpenScaleClient.subscription.feedback_logging.describe_table()
        TestAIOpenScaleClient.subscription.feedback_logging.get_table_content()
        feedback_logging = TestAIOpenScaleClient.subscription.feedback_logging.get_table_content(format='python')
        self.assertTrue(len(feedback_logging['values']) > 0)

    def test_12_disable_quality_monitoring(self):
        TestAIOpenScaleClient.subscription.quality_monitoring.disable()

    def test_13_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='quality'))
        print(TestAIOpenScaleClient.subscription.quality_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))

        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid, metric_type='quality')['deployment_metrics'][0]['metrics']) > 0)
        self.assertTrue(len(TestAIOpenScaleClient.subscription.quality_monitoring.get_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid)['metrics']) > 0)

    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_16_clean(self):
        self.wml_client.repository.delete(TestAIOpenScaleClient.model_uid)

    def test_17_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)

    # def test_18_delete_data_mart(self):
    #     for uid in TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids():
    #         TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(uid)
    #     TestAIOpenScaleClient.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
