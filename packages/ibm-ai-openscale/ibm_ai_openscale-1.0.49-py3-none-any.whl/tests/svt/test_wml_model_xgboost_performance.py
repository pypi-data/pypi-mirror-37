import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import XGboost

class TestWMLModelXgboostPerformance(unittest.TestCase):
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
        TestWMLModelXgboostPerformance.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestWMLModelXgboostPerformance.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestWMLModelXgboostPerformance.binding_id = TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.add("Xgboost performance instance", WatsonMachineLearningInstance(self.wml_credentials))
        print("Datamart binding guid: {}".format(TestWMLModelXgboostPerformance.binding_id))
        self.assertIsNotNone(TestWMLModelXgboostPerformance.binding_id)

    def test_04_get_wml_client(self):
        TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.list()
        binding_uid = TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.get_uids()[0]
        print("Datamart details binding guid: {}".format(binding_uid))
        self.assertIsNotNone(binding_uid)
        self.assertEqual(binding_uid, TestWMLModelXgboostPerformance.binding_id)
        TestWMLModelXgboostPerformance.wml_client = TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)
        self.assertIsNotNone(TestWMLModelXgboostPerformance.wml_client)

    def test_05_1_store_model(self):

        model_meta_props = {
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            self.wml_client.repository.ModelMetaNames.AUTHOR_EMAIL: "ibm@ibm.com",
            self.wml_client.repository.ModelMetaNames.NAME: "LOCALLY created agaricus prediction model",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "xgboost",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "0.6"
        }
        published_model_details = self.wml_client.repository.store_model(model=XGboost.get_model_data()['path'], meta_props=model_meta_props)
        print("Published model details: {}".format(published_model_details))
        TestWMLModelXgboostPerformance.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        print("Published model ID: {}".format(TestWMLModelXgboostPerformance.model_uid))
        self.assertIsNotNone(TestWMLModelXgboostPerformance.model_uid)

    def test_05_2_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestWMLModelXgboostPerformance.model_uid, name="XGboost AIOS Deployment", asynchronous=False)
        TestWMLModelXgboostPerformance.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        print("Deployment ID: {}".format(TestWMLModelXgboostPerformance.deployment_uid))
        self.assertIsNotNone(TestWMLModelXgboostPerformance.deployment_uid)
        TestWMLModelXgboostPerformance.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        print("Scoring url: {}".format(TestWMLModelXgboostPerformance.scoring_url))
        self.assertTrue('online' in str(TestWMLModelXgboostPerformance.scoring_url))

    def test_06_subscribe(self):
        subscription = TestWMLModelXgboostPerformance.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestWMLModelXgboostPerformance.model_uid))
        TestWMLModelXgboostPerformance.subscription_uid = subscription.uid
        print("Subscription ID: {}".format(TestWMLModelXgboostPerformance.subscription_uid))
        self.assertIsNotNone(TestWMLModelXgboostPerformance.subscription_uid)

    def test_07_select_asset_and_get_details(self):
        TestWMLModelXgboostPerformance.subscription = TestWMLModelXgboostPerformance.ai_client.data_mart.subscriptions.get(TestWMLModelXgboostPerformance.subscription_uid)
        self.assertIsNotNone(TestWMLModelXgboostPerformance.subscription)
        print("Subscription details before performance monitoring:\n{}".format(TestWMLModelXgboostPerformance.subscription.get_details()))

    def test_08_setup_performance_monitoring(self):
        TestWMLModelXgboostPerformance.subscription.performance_monitoring.enable()
        print("Subscription details after performance monitor ON:\n{}".format(TestWMLModelXgboostPerformance.subscription.get_details()))

    def test_09_get_performance_monitoring_details(self):
        performance_monitoring_details = TestWMLModelXgboostPerformance.subscription.performance_monitoring.get_details()
        print("Performance monitoring details:\n{}".format(performance_monitoring_details))

    def test_10_score(self):
        print("Scoring model ...")

        scoring_data = XGboost.get_scoring_payload()

        self.wml_client.deployments.score(scoring_url=TestWMLModelXgboostPerformance.scoring_url, payload=scoring_data)
        self.wml_client.deployments.score(scoring_url=TestWMLModelXgboostPerformance.scoring_url, payload=scoring_data)
        self.wml_client.deployments.score(scoring_url=TestWMLModelXgboostPerformance.scoring_url, payload=scoring_data)
        scores = self.wml_client.deployments.score(scoring_url=TestWMLModelXgboostPerformance.scoring_url, payload=scoring_data)

        self.assertIsNotNone(scores)

        import time

        print("Scoring completed. Waiting 2 minutes for propagation.")
        time.sleep(120)

    def test_11_stats_on_performance_monitoring_table(self):
        print("Printing performance table: ")
        TestWMLModelXgboostPerformance.subscription.performance_monitoring.print_table_schema()
        TestWMLModelXgboostPerformance.subscription.performance_monitoring.show_table()
        TestWMLModelXgboostPerformance.subscription.performance_monitoring.describe_table()
        TestWMLModelXgboostPerformance.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestWMLModelXgboostPerformance.subscription.performance_monitoring.get_table_content(format='python')
        print("Performance metrics:\n{}".format(performance_metrics))
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_performance_monitoring(self):
        TestWMLModelXgboostPerformance.subscription.fairness_monitoring.disable()

    def test_13_get_metrics(self):
        deployment_metrics = TestWMLModelXgboostPerformance.ai_client.data_mart.get_deployment_metrics()
        deployment_metrics_deployment_uid = TestWMLModelXgboostPerformance.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestWMLModelXgboostPerformance.deployment_uid)
        deployment_metrics_subscription_uid = TestWMLModelXgboostPerformance.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestWMLModelXgboostPerformance.subscription.uid)
        deployment_metrics_asset_id = TestWMLModelXgboostPerformance.ai_client.data_mart.get_deployment_metrics(asset_uid=TestWMLModelXgboostPerformance.subscription.source_uid)
        deployment_metrics_quality = TestWMLModelXgboostPerformance.ai_client.data_mart.get_deployment_metrics(metric_type='quality')
        performance_metrics = TestWMLModelXgboostPerformance.subscription.performance_monitoring.get_metrics(deployment_uid=TestWMLModelXgboostPerformance.deployment_uid)

        print("Deployment metrics:\n{}".format(deployment_metrics))
        print("Deployment metrics deployment uid:\n{}".format(deployment_metrics_deployment_uid))
        print("Deployment metrics subscription uid:\n{}".format(deployment_metrics_subscription_uid))
        print("Deployment metrics asset uid:\n{}".format(deployment_metrics_asset_id))
        print("Deployment metrics quality:\n{}".format(deployment_metrics_quality))
        print("Performance monitoring metrics:\n{}".format(performance_metrics))

        self.assertGreater(len(deployment_metrics), 0)
        self.assertGreater(len(deployment_metrics_deployment_uid), 0)
        self.assertGreater(len(deployment_metrics_subscription_uid), 0)
        self.assertGreater(len(deployment_metrics_asset_id), 0)
        self.assertGreater(len(performance_metrics), 0)

    def test_14_unsubscribe(self):
        TestWMLModelXgboostPerformance.ai_client.data_mart.subscriptions.delete(TestWMLModelXgboostPerformance.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestWMLModelXgboostPerformance.deployment_uid)
        self.wml_client.repository.delete(TestWMLModelXgboostPerformance.model_uid)

    def test_16_unbind(self):
        TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.delete(TestWMLModelXgboostPerformance.subscription.binding_uid)

    # def test_17_delete_data_mart(self):
    #     for uid in TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.get_uids():
    #         TestWMLModelXgboostPerformance.ai_client.data_mart.bindings.delete(uid)
    #     TestWMLModelXgboostPerformance.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
