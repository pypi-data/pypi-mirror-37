import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import SPSSCustomerSatisfaction


class TestSPSSPerformance(unittest.TestCase):
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

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestSPSSPerformance.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestSPSSPerformance.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials,
                                                      schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestSPSSPerformance.ai_client.data_mart.bindings.add("My WML instance",
                                                             WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        TestSPSSPerformance.ai_client.data_mart.bindings.list()
        binding_uid = TestSPSSPerformance.ai_client.data_mart.bindings.get_uids()[0]
        TestSPSSPerformance.wml_client = TestSPSSPerformance.ai_client.data_mart.bindings.get_native_engine_client(
            binding_uid)

    def test_05_1_store_model(self):
        model_meta_props = {
            self.wml_client.repository.ModelMetaNames.NAME: "SPSS customer sample model",
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "John Smith",
            self.wml_client.repository.ModelMetaNames.AUTHOR_EMAIL: "js@js.com",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "spss-modeler",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "18.0",
            self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "spss-modeler",
            self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "18.0"
        }
        published_model_details = self.wml_client.repository.store_model(
            model=SPSSCustomerSatisfaction.get_model_data()['path'], meta_props=model_meta_props)
        TestSPSSPerformance.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        TestSPSSPerformance.logger.info("Published model ID:" + str(TestSPSSPerformance.model_uid))
        self.assertIsNotNone(TestSPSSPerformance.model_uid)

    def test_05_2_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestSPSSPerformance.model_uid,
                                                                name="SPSS AIOS Deployment", asynchronous=False)
        TestSPSSPerformance.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        TestSPSSPerformance.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestSPSSPerformance.scoring_url))

    def test_06_subscribe(self):
        subscription = TestSPSSPerformance.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestSPSSPerformance.model_uid))
        TestSPSSPerformance.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestSPSSPerformance.subscription = TestSPSSPerformance.ai_client.data_mart.subscriptions.get(
            TestSPSSPerformance.aios_model_uid)
        print(str(TestSPSSPerformance.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestSPSSPerformance.subscription.list_deployments()

    def test_08_setup_performance_monitoring(self):
        TestSPSSPerformance.subscription.performance_monitoring.enable()
        print('Subscription details after performance monitor ON: ' + str(
            TestSPSSPerformance.subscription.get_details()))

    def test_09_get_performance_monitoring_details(self):
        TestSPSSPerformance.subscription.performance_monitoring.get_details()

    def test_10_score(self):
        print("Scoring model.")

        scoring_payload = SPSSCustomerSatisfaction.get_scoring_payload()

        self.wml_client.deployments.score(scoring_url=TestSPSSPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestSPSSPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestSPSSPerformance.scoring_url, payload=scoring_payload)
        scores = self.wml_client.deployments.score(scoring_url=TestSPSSPerformance.scoring_url,
                                                   payload=scoring_payload)

        self.assertIsNotNone(scores)

        print("Scoring finished. Waining 2 minutes for propagation.")
        import time
        time.sleep(120)

    def test_11_stats_on_performance_monitoring_table(self):
        TestSPSSPerformance.subscription.performance_monitoring.print_table_schema()
        TestSPSSPerformance.subscription.performance_monitoring.show_table()
        TestSPSSPerformance.subscription.performance_monitoring.describe_table()
        TestSPSSPerformance.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestSPSSPerformance.subscription.performance_monitoring.get_table_content(
            format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_performance_monitoring(self):
        TestSPSSPerformance.subscription.fairness_monitoring.disable()

    def test_13_get_metrics(self):
        print(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics())
        print(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestSPSSPerformance.deployment_uid))
        print(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestSPSSPerformance.subscription.uid))
        print(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSPSSPerformance.subscription.source_uid))
        print(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSPSSPerformance.subscription.source_uid, metric_type='quality'))
        print(TestSPSSPerformance.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestSPSSPerformance.deployment_uid))

        self.assertTrue(
            len(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics()['deployment_metrics']) > 0)
        self.assertTrue(len(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            deployment_uid=TestSPSSPerformance.deployment_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            subscription_uid=TestSPSSPerformance.subscription.uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSPSSPerformance.subscription.source_uid)['deployment_metrics']) > 0)
        self.assertTrue(len(TestSPSSPerformance.ai_client.data_mart.get_deployment_metrics(
            asset_uid=TestSPSSPerformance.subscription.source_uid, metric_type='performance')['deployment_metrics'][
                                0]['metrics']) > 0)
        self.assertTrue(len(TestSPSSPerformance.subscription.performance_monitoring.get_metrics(
            deployment_uid=TestSPSSPerformance.deployment_uid)['metrics']) > 0)

    def test_14_unsubscribe(self):
        TestSPSSPerformance.ai_client.data_mart.subscriptions.delete(TestSPSSPerformance.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestSPSSPerformance.deployment_uid)
        self.wml_client.repository.delete(TestSPSSPerformance.model_uid)

    def test_16_unbind(self):
        TestSPSSPerformance.ai_client.data_mart.bindings.delete(TestSPSSPerformance.subscription.binding_uid)

    # def test_17_delete_data_mart(self):
    #     for uid in TestSPSSPerformance.ai_client.data_mart.bindings.get_uids():
    #         TestSPSSPerformance.ai_client.data_mart.bindings.delete(uid)
    #     TestSPSSPerformance.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
