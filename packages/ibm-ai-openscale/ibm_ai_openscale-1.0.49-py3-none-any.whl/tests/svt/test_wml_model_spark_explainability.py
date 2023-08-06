import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import *
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

        self.cos_resource = get_cos_resource()
        self.bucket_names = prepare_cos(self.cos_resource, data_code=GO_SALES)

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestAIOpenScaleClient.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestAIOpenScaleClient.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestAIOpenScaleClient.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_uids()[0]
        TestAIOpenScaleClient.wml_client = TestAIOpenScaleClient.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_deployment(self):
        model_data = create_spark_mllib_model_data()

        model_props = {self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                       self.wml_client.repository.ModelMetaNames.NAME: "test_" + self.test_uid
                       }

        published_model = self.wml_client.repository.store_model(model=model_data['model'], meta_props=model_props,
                                                                 training_data=model_data['training_data'],
                                                                 pipeline=model_data['pipeline'])
        TestAIOpenScaleClient.model_uid = self.wml_client.repository.get_model_uid(published_model)

        print('Stored model: ', TestAIOpenScaleClient.model_uid)

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestAIOpenScaleClient.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestAIOpenScaleClient.model_uid))
        TestAIOpenScaleClient.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestAIOpenScaleClient.subscription = TestAIOpenScaleClient.ai_client.data_mart.subscriptions.get(TestAIOpenScaleClient.aios_model_uid)

    def test_07b_list_deployments(self):
        TestAIOpenScaleClient.subscription.list_deployments()

    def test_08_setup_explainability(self):
        TestAIOpenScaleClient.subscription._explainability.enable(
            ExplainabilityModelType.CLASSIFICATION,
            ExplainabilityModelDataType.NUMERIC_CATEGORICAL,
            feature_columns=["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"],
            label_column='label',
            training_data_reference=BluemixCloudObjectStorageReference(
                get_cos_credentials(),
                self.bucket_names['data'] + '/GoSales_Tx_NaiveBayes.csv',
                first_line_header=True
            ),
            categorical_columns=["GENDER", "MARITAL_STATUS", "PROFESSION"]
        )

    def test_09_get_explainability_details(self):
        TestAIOpenScaleClient.subscription._explainability.get_details()

    def test_10_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestAIOpenScaleClient.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = {"fields": ["GENDER", "AGE", "MARITAL_STATUS", "PROFESSION"],
                           "values": [["M", 23, "Single", "Student"], ["M", 55, "Single", "Executive"]]}

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        import time
        time.sleep(30)

    def test_11_run(self):
        transaction_id = TestAIOpenScaleClient.subscription.payload_logging.get_table_content(format='python')['values'][0][0]
        status = TestAIOpenScaleClient.subscription._explainability.run(transaction_id)

        TestAIOpenScaleClient.subscription._explainability.show_table()
        TestAIOpenScaleClient.subscription._explainability.describe_table()
        pandas_df = TestAIOpenScaleClient.subscription._explainability.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)
        self.assertTrue(status == 'finished')

    def test_11b_print_schema(self):
        TestAIOpenScaleClient.subscription._explainability.print_table_schema()

    def test_12_disable_explainability(self):
        TestAIOpenScaleClient.subscription._explainability.disable()

    def test_13_get_metrics(self):
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics())
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestAIOpenScaleClient.deployment_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestAIOpenScaleClient.subscription.uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(asset_uid=TestAIOpenScaleClient.subscription.source_uid))
        print(TestAIOpenScaleClient.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

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
