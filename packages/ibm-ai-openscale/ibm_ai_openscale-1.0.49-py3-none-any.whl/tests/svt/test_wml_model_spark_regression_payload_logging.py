import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import SparkMlibRegression


class TestSparkRegressionPayloadLogging(unittest.TestCase):
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
        TestSparkRegressionPayloadLogging.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestSparkRegressionPayloadLogging.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestSparkRegressionPayloadLogging.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials,
                                                                    schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.add("My WML instance",
                                                                           WatsonMachineLearningInstance(
                                                                               self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.get_uids()[0]
        TestSparkRegressionPayloadLogging.wml_client = TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)

    def test_05_prepare_deployment(self):
        model_data = SparkMlibRegression.get_model_data()

        model_props = {
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            self.wml_client.repository.ModelMetaNames.NAME: "test_" + self.test_uid
        }

        published_model = self.wml_client.repository.store_model(model=model_data['model'], meta_props=model_props,
                                                                 training_data=model_data['training_data'],
                                                                 pipeline=model_data['pipeline'])
        TestSparkRegressionPayloadLogging.model_uid = self.wml_client.repository.get_model_uid(published_model)

        print('Stored model: ', TestSparkRegressionPayloadLogging.model_uid)

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestSparkRegressionPayloadLogging.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestSparkRegressionPayloadLogging.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestSparkRegressionPayloadLogging.model_uid))
        TestSparkRegressionPayloadLogging.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestSparkRegressionPayloadLogging.subscription = TestSparkRegressionPayloadLogging.ai_client.data_mart.subscriptions.get(
            TestSparkRegressionPayloadLogging.aios_model_uid)
        print('Subscription details: ' + str(TestSparkRegressionPayloadLogging.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestSparkRegressionPayloadLogging.subscription.list_deployments()

    def test_08_setup_payload_logging(self):
        TestSparkRegressionPayloadLogging.subscription.payload_logging.enable()

    def test_09_get_payload_logging_details(self):
        payload_logging_details = TestSparkRegressionPayloadLogging.subscription.payload_logging.get_details()
        print(str(payload_logging_details))

    def test_10_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestSparkRegressionPayloadLogging.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = SparkMlibRegression.get_scoring_payload()

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)

    def test_11_stats_on_payload_logging_table(self):
        TestSparkRegressionPayloadLogging.subscription.payload_logging.print_table_schema()
        TestSparkRegressionPayloadLogging.subscription.payload_logging.show_table()
        TestSparkRegressionPayloadLogging.subscription.payload_logging.describe_table()
        pandas_df = TestSparkRegressionPayloadLogging.subscription.payload_logging.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)

    def test_12_disable_payload_logging(self):
        TestSparkRegressionPayloadLogging.subscription.payload_logging.disable()

    def test_13_get_metrics(self):
        print(TestSparkRegressionPayloadLogging.ai_client.data_mart.get_deployment_metrics())
        print(TestSparkRegressionPayloadLogging.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestSparkRegressionPayloadLogging.deployment_uid))
        print(TestSparkRegressionPayloadLogging.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestSparkRegressionPayloadLogging.subscription.uid))
        print(TestSparkRegressionPayloadLogging.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSparkRegressionPayloadLogging.subscription.source_uid))
        print(TestSparkRegressionPayloadLogging.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_14_unsubscribe(self):
        TestSparkRegressionPayloadLogging.ai_client.data_mart.subscriptions.delete(
            TestSparkRegressionPayloadLogging.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestSparkRegressionPayloadLogging.deployment_uid)
        self.wml_client.repository.delete(TestSparkRegressionPayloadLogging.model_uid)

    def test_16_unbind(self):
        TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.delete(TestSparkRegressionPayloadLogging.subscription.binding_uid)

    # def test_17_delete_data_mart(self):
    #     for uid in TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.get_uids():
    #         TestSparkRegressionPayloadLogging.ai_client.data_mart.bindings.delete(uid)
    #     TestSparkRegressionPayloadLogging.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
