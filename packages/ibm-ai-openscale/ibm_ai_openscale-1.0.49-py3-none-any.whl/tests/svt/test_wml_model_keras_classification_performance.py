import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from preparation_and_cleaning import *
from models import KerasVGG16


class TestKerasClassificationPerformance(unittest.TestCase):
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
        TestKerasClassificationPerformance.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestKerasClassificationPerformance.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestKerasClassificationPerformance.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestKerasClassificationPerformance.ai_client.data_mart.bindings.get_uids()[0]
        TestKerasClassificationPerformance.wml_client = TestKerasClassificationPerformance.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_1_publish_model(self):
        model_props = {
            self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
            self.wml_client.repository.ModelMetaNames.NAME: "CAT DOG",
            self.wml_client.repository.ModelMetaNames.DESCRIPTION: "CAT DOG model",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.5",
            self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
            self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.5",
            self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [
                {"name": "keras", "version": "2.1.3"}
            ]
        }

        published_model_details = self.wml_client.repository.store_model(model=KerasVGG16.get_model_data()['path'],
                                                                         meta_props=model_props)
        TestKerasClassificationPerformance.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        TestKerasClassificationPerformance.model_url = self.wml_client.repository.get_model_url(published_model_details)
        print("Published model ID:" + str(TestKerasClassificationPerformance.model_uid))
        print("Published model URL:" + str(TestKerasClassificationPerformance.model_url))
        self.assertIsNotNone(TestKerasClassificationPerformance.model_uid)
        self.assertIsNotNone(TestKerasClassificationPerformance.model_url)

    def test_05_2_create_deployment(self):
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestKerasClassificationPerformance.model_uid,
                                                                name="Keras VGG", asynchronous=False)
        TestKerasClassificationPerformance.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        TestKerasClassificationPerformance.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestKerasClassificationPerformance.scoring_url))

    def test_06_subscribe(self):
        subscription = TestKerasClassificationPerformance.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestKerasClassificationPerformance.model_uid))
        TestKerasClassificationPerformance.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestKerasClassificationPerformance.subscription = TestKerasClassificationPerformance.ai_client.data_mart.subscriptions.get(
            TestKerasClassificationPerformance.aios_model_uid)
        print(str(TestKerasClassificationPerformance.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestKerasClassificationPerformance.subscription.list_deployments()

    def test_08_setup_performance_monitoring(self):
        TestKerasClassificationPerformance.subscription.performance_monitoring.enable()
        print('Subscription details after performance monitor ON: ' + str(
            TestKerasClassificationPerformance.subscription.get_details()))

    def test_09_get_performance_monitor_details(self):
        TestKerasClassificationPerformance.subscription.performance_monitoring.get_details()

    def test_10_score(self):
        print("Scoring deployment.")

        scoring_payload = KerasVGG16.get_scoring_payload()

        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url, payload=scoring_payload)
        scores = self.wml_client.deployments.score(scoring_url=TestKerasClassificationPerformance.scoring_url,
                                                   payload=scoring_payload)

        self.assertIsNotNone(scores)

        import time
        time.sleep(120)

    def test_11_stats_on_performance_monitoring_table(self):
        TestKerasClassificationPerformance.subscription.performance_monitoring.print_table_schema()
        TestKerasClassificationPerformance.subscription.performance_monitoring.show_table()
        TestKerasClassificationPerformance.subscription.performance_monitoring.describe_table()
        TestKerasClassificationPerformance.subscription.performance_monitoring.get_table_content()
        performance_metrics = TestKerasClassificationPerformance.subscription.performance_monitoring.get_table_content(format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_performance_monitoring(self):
        TestKerasClassificationPerformance.subscription.performance_monitoring.disable()

    def test_13_get_metrics(self):
        print(TestKerasClassificationPerformance.subscription.performance_monitoring.get_metrics(deployment_uid=TestKerasClassificationPerformance.deployment_uid))

        self.assertTrue(len(TestKerasClassificationPerformance.subscription.performance_monitoring.get_metrics(deployment_uid=TestKerasClassificationPerformance.deployment_uid)['metrics']) > 0)

    def test_14_unsubscribe(self):
        TestKerasClassificationPerformance.ai_client.data_mart.subscriptions.delete(TestKerasClassificationPerformance.subscription.uid)

    # def test_15_clean(self):
    #     self.wml_client.deployments.delete(TestKerasClassificationPerformance.deployment_uid)
    #     self.wml_client.repository.delete(TestKerasClassificationPerformance.model_uid)

    def test_15_unbind(self):
        TestKerasClassificationPerformance.ai_client.data_mart.bindings.delete(TestKerasClassificationPerformance.subscription.binding_uid)

    # def test_16_delete_data_mart(self):
    #     for uid in TestKerasClassificationPerformance.ai_client.data_mart.bindings.get_uids():
    #         TestKerasClassificationPerformance.ai_client.data_mart.bindings.delete(uid)
    #     TestKerasClassificationPerformance.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
