import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.utils import *
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
    binding_uid = None

    @classmethod
    def setUpClass(self):
        TestAIOpenScaleClient.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_data_mart_get_details(self):
        details = TestAIOpenScaleClient.ai_client.data_mart.get_details()
        print(details)
        self.assertTrue(len(json.dumps(details)) > 10)

    def test_04_bind_generic_instance(self):
        TestAIOpenScaleClient.binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My generic instance", GenericMachineLearningInstance())

    def test_05_get_wml_client(self):
        self.assertRaises(ClientError, TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client, TestAIOpenScaleClient.binding_uid)

    def test_06_list_instances(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list()

    def test_07_get_uids(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()

    def test_08_get_details(self):
        print('DETAILS', TestAIOpenScaleClient.ai_client.data_mart.bindings.get_details())

    def test_09_list_subscriptions(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()

    def test_10_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(
            GenericAsset(name="test_" + self.test_uid, source_url='test', binding_uid=TestAIOpenScaleClient.binding_uid)
        )
        TestAIOpenScaleClient.aios_model_uid = subscription.uid
        # TODO check the deployments

    def test_11_list_and_get_uids_after_subscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list()
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.list(name='test_' + self.test_uid)
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get_uids()

    def test_12_check_if_deployments_were_added(self):
        self.assertTrue(len(TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get_details()['subscriptions'][0]['entity']['deployments']) > 0)

    def test_13_list_models_and_functions(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.list_assets()

    def test_14_get_asset_uids(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.get_asset_uids()

    def test_15_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='test_' + TestAIOpenScaleClient.test_uid, choose='random')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='test_' + TestAIOpenScaleClient.test_uid, choose='first')
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(name='test_' + TestAIOpenScaleClient.test_uid, choose='last')
        TestAIOpenScaleClient.subscription.get_details()

    def test_15b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_16_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_17_unsubscribe(self):
        TestAIOpenScaleClient.ai_client.data_mart.subscriptions.delete(TestAIOpenScaleClient.subscription.uid)

    def test_18_unbind(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(TestAIOpenScaleClient.subscription.binding_uid)

    # def test_19_delete_data_mart(self):
    #     for uid in TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids():
    #         TestAIOpenScaleClient.ai_client.data_mart.bindings.delete(uid)
    #     TestAIOpenScaleClient.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
