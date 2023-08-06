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
        self.model_path = os.path.join(os.getcwd(), 'artifacts', 'core_ml', 'keras', 'mnistCNN.h5.tgz')

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_1__publish_model(self):

        self.logger.info("Publishing Keras model ...")

        model_props = {
                        self.wml_client.repository.ModelMetaNames.NAME: "Keras mnist model",
                        self.wml_client.repository.ModelMetaNames.FRAMEWORK_NAME: "tensorflow",
                        self.wml_client.repository.ModelMetaNames.FRAMEWORK_VERSION: "1.5",
                        self.wml_client.repository.ModelMetaNames.RUNTIME_NAME: "python",
                        self.wml_client.repository.ModelMetaNames.RUNTIME_VERSION: "3.5",
                        self.wml_client.repository.ModelMetaNames.FRAMEWORK_LIBRARIES: [{'name':'keras', 'version': '2.1.3'}],
        }

        published_model_details = self.wml_client.repository.store_model(model=self.model_path, meta_props=model_props)
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model_details)
        TestAIOpenScaleClient.model_url = self.wml_client.repository.get_model_url(published_model_details)
        self.logger.info("Published model ID:" + str(TestAIOpenScaleClient.model_uid))
        self.logger.info("Published model URL:" + str(TestAIOpenScaleClient.model_url))
        self.assertIsNotNone(TestAIOpenScaleClient.model_uid)
        self.assertIsNotNone(TestAIOpenScaleClient.model_url)

    def test_05_2_create_deployment(self):
        TestAIOpenScaleClient.logger.info("Create deployment")
        deployment_details = self.wml_client.deployments.create(artifact_uid=TestAIOpenScaleClient.model_uid,
                                                                name="Test deployment", asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment_details)
        TestAIOpenScaleClient.scoring_url = self.wml_client.deployments.get_scoring_url(deployment_details)
        self.assertTrue('online' in str(TestAIOpenScaleClient.scoring_url))

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(
            TestAIOpenScaleClient.aios_model_uid)
        print(str(TestAIOpenScaleClient.subscription.get_details()))

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.enable()
        print('Subscription details after payload logging ON: ' + str(
            TestAIOpenScaleClient.subscription.get_details()))

    def test_09_get_payload_logging_details(self):
        TestAIOpenScaleClient.subscription.payload_logging.get_details()

    def test_10_score(self):
        TestAIOpenScaleClient.logger.info("Score model")

        from keras.datasets import mnist
        import numpy as np

        (x_train, y_train), (x_test, y_test) = mnist.load_data()

        image_1 = np.expand_dims(x_test[0], axis=2)
        image_2 = np.expand_dims(x_test[1], axis=2)

        print('Image: ' + str(image_1.tolist()))
        print('Image: ' + str(image_2.tolist()))

        scoring_payload = {'values': [image_1.tolist(), image_2.tolist()]}

        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url, payload=scoring_payload)
        scores = self.wml_client.deployments.score(scoring_url=TestAIOpenScaleClient.scoring_url,
                                                   payload=scoring_payload)

        self.assertIsNotNone(scores)

        import time
        time.sleep(10)

    def test_11_stats_on_payload_logging_table(self):
        TestAIOpenScaleClient.subscription.payload_logging.print_table_schema()
        TestAIOpenScaleClient.subscription.payload_logging.show_table()
        TestAIOpenScaleClient.subscription.payload_logging.describe_table()
        TestAIOpenScaleClient.subscription.payload_logging.get_table_content()
        performance_metrics = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')
        self.assertTrue(len(performance_metrics['values']) > 0)

    def test_12_disable_payload_logging(self):
        TestAIOpenScaleClient.subscription.payload_logging.disable()

    def test_15_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_16_clean(self):
        self.wml_client.deployments.delete(TestAIOpenScaleClient.deployment_uid)
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