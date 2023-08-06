import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import SparkMlibRegression


class TestSparkRegressionPerformance(unittest.TestCase):
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
        TestSparkRegressionPerformance.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestSparkRegressionPerformance.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestSparkRegressionPerformance.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials,
                                                                 schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestSparkRegressionPerformance.ai_client.data_mart.bindings.add("My WML instance",
                                                                        WatsonMachineLearningInstance(
                                                                            self.wml_credentials))

    def test_04_get_wml_client(self):
        TestSparkRegressionPerformance.ai_client.data_mart.bindings.list()
        binding_uid = TestSparkRegressionPerformance.ai_client.data_mart.bindings.get_uids()[0]
        TestSparkRegressionPerformance.wml_client = TestSparkRegressionPerformance.ai_client.data_mart.bindings.get_native_engine_client(
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
        TestSparkRegressionPerformance.model_uid = self.wml_client.repository.get_model_uid(published_model)

        print('Stored model: ', TestSparkRegressionPerformance.model_uid)

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestSparkRegressionPerformance.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestSparkRegressionPerformance.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestSparkRegressionPerformance.model_uid))
        TestSparkRegressionPerformance.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestSparkRegressionPerformance.subscription = TestSparkRegressionPerformance.ai_client.data_mart.subscriptions.get(
            TestSparkRegressionPerformance.aios_model_uid)
        print(str(TestSparkRegressionPerformance.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestSparkRegressionPerformance.subscription.list_deployments()

    def test_08_setup_performance_monitoring(self):
        TestSparkRegressionPerformance.subscription.performance_monitoring.enable()
        print('Subscription details after performance monitor ON: ' + str(
            TestSparkRegressionPerformance.subscription.get_details()))

    def test_09_get_performance_monitoring_details(self):
        TestSparkRegressionPerformance.subscription.performance_monitoring.get_details()

    def test_10_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestSparkRegressionPerformance.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = SparkMlibRegression.get_scoring_payload()

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)

        import time
        time.sleep(120)

    def test_11_stats_on_performance_monitoring_table(self):
        TestSparkRegressionPerformance.subscription.performance_monitoring.print_table_schema()
        TestSparkRegressionPerformance.subscription.performance_monitoring.show_table()
        TestSparkRegressionPerformance.subscription.performance_monitoring.describe_table()
        TestSparkRegressionPerformance.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestSparkRegressionPerformance.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_performance_monitoring(self):
        TestSparkRegressionPerformance.subscription.fairness_monitoring.disable()

    def test_13_get_metrics(self):
        print(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics())
        print(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestSparkRegressionPerformance.deployment_uid))
        print(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestSparkRegressionPerformance.subscription.uid))
        print(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSparkRegressionPerformance.subscription.source_uid))
        print(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSparkRegressionPerformance.subscription.source_uid, metric_type='quality'))
        print(TestSparkRegressionPerformance.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestSparkRegressionPerformance.deployment_uid))

        self.assertTrue(
            len(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestSparkRegressionPerformance.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestSparkRegressionPerformance.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSparkRegressionPerformance.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSparkRegressionPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSparkRegressionPerformance.subscription.source_uid, metric_type='performance')[
                                'deployment_metrics'][0]['metrics']) > 0)
        self.assertTrue(len(TestSparkRegressionPerformance.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestSparkRegressionPerformance.deployment_uid)['metrics']) > 0)

    def test_14_unsubscribe(self):
        TestSparkRegressionPerformance.ai_client.data_mart.subscriptions.delete(
            TestSparkRegressionPerformance.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestSparkRegressionPerformance.deployment_uid)
        self.wml_client.repository.delete(TestSparkRegressionPerformance.model_uid)

    def test_16_unbind(self):
        TestSparkRegressionPerformance.ai_client.data_mart.bindings.delete(TestSparkRegressionPerformance.subscription.binding_uid)

    # def test_17_delete_data_mart(self):
    #     for uid in TestSparkRegressionPerformance.ai_client.data_mart.bindings.get_uids():
    #         TestSparkRegressionPerformance.ai_client.data_mart.bindings.delete(uid)
    #     TestSparkRegressionPerformance.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
