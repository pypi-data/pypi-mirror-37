import logging
import unittest

from ibm_ai_openscale import APIClient
from ibm_ai_openscale.engines import *
from ibm_ai_openscale.supporting_classes import *
from preparation_and_cleaning import *
from models import SparkMlibRegression


class TestSparkRegressionExplainability(unittest.TestCase):
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
        TestSparkRegressionExplainability.logger.info("Service Instance: setting up credentials")

        clean_env()

        self.cos_resource = get_cos_resource()
        self.bucket_names = prepare_cos(self.cos_resource, data_code=GO_SALES)

        self.aios_credentials = get_aios_credentials()
        self.wml_credentials = get_wml_credentials()
        self.postgres_credentials = get_postgres_credentials()

    def test_01_create_client(self):
        TestSparkRegressionExplainability.ai_client = APIClient(self.aios_credentials)

    def test_02_setup_data_mart(self):
        TestSparkRegressionExplainability.ai_client.data_mart.setup(postgres_credentials=self.postgres_credentials, schema=get_schema_name())

    def test_03_bind_wml_instance_and_get_wml_client(self):
        TestSparkRegressionExplainability.ai_client.data_mart.bindings.add("My WML instance", WatsonMachineLearningInstance(self.wml_credentials))

    def test_04_get_wml_client(self):
        binding_uid = TestSparkRegressionExplainability.ai_client.data_mart.bindings.get_uids()[0]
        TestSparkRegressionExplainability.wml_client = TestSparkRegressionExplainability.ai_client.data_mart.bindings.get_native_engine_client(binding_uid)

    def test_05_prepare_deployment(self):
        model_data = SparkMlibRegression.get_model_data()

        model_props = {self.wml_client.repository.ModelMetaNames.AUTHOR_NAME: "IBM",
                       self.wml_client.repository.ModelMetaNames.NAME: "test_" + self.test_uid
                       }

        published_model = self.wml_client.repository.store_model(model=model_data['model'], meta_props=model_props,
                                                                 training_data=model_data['training_data'],
                                                                 pipeline=model_data['pipeline'])
        TestSparkRegressionExplainability.model_uid = self.wml_client.repository.get_model_uid(published_model)

        print('Stored model: ', TestSparkRegressionExplainability.model_uid)

        deployment = self.wml_client.deployments.create(artifact_uid=self.model_uid, name="Test deployment",
                                                        asynchronous=False)
        TestSparkRegressionExplainability.deployment_uid = self.wml_client.deployments.get_uid(deployment)

    def test_06_subscribe(self):
        subscription = TestSparkRegressionExplainability.ai_client.data_mart.subscriptions.add(WatsonMachineLearningAsset(TestSparkRegressionExplainability.model_uid))
        TestSparkRegressionExplainability.aios_model_uid = subscription.uid

    def test_07_select_asset_and_get_details(self):
        TestSparkRegressionExplainability.subscription = TestSparkRegressionExplainability.ai_client.data_mart.subscriptions.get(TestSparkRegressionExplainability.aios_model_uid)

    def test_07b_list_deployments(self):
        TestSparkRegressionExplainability.subscription.list_deployments()

    def test_08_setup_explainability(self):
        TestSparkRegressionExplainability.subscription._explainability.enable(
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
        TestSparkRegressionExplainability.subscription._explainability.get_details()

    def test_10_score(self):
        deployment_details = self.wml_client.deployments.get_details(TestSparkRegressionExplainability.deployment_uid)
        scoring_endpoint = self.wml_client.deployments.get_scoring_url(deployment_details)

        payload_scoring = SparkMlibRegression.get_scoring_payload()

        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        self.wml_client.deployments.score(scoring_endpoint, payload_scoring)
        import time
        time.sleep(30)

    def test_11_run(self):
        transaction_id = TestSparkRegressionExplainability.subscription.payload_logging.get_table_content(format='python')['values'][0][0]
        status = TestSparkRegressionExplainability.subscription._explainability.run(transaction_id)

        TestSparkRegressionExplainability.subscription._explainability.show_table()
        TestSparkRegressionExplainability.subscription._explainability.describe_table()
        pandas_df = TestSparkRegressionExplainability.subscription._explainability.get_table_content()
        print(str(pandas_df))
        self.assertTrue(pandas_df.size > 1)
        self.assertTrue(status == 'finished')

    def test_11b_print_schema(self):
        TestSparkRegressionExplainability.subscription._explainability.print_table_schema()

    def test_12_disable_explainability(self):
        TestSparkRegressionExplainability.subscription._explainability.disable()

    def test_13_get_metrics(self):
        print(TestSparkRegressionExplainability.ai_client.data_mart.get_deployment_metrics())
        print(TestSparkRegressionExplainability.ai_client.data_mart.get_deployment_metrics(deployment_uid=TestSparkRegressionExplainability.deployment_uid))
        print(TestSparkRegressionExplainability.ai_client.data_mart.get_deployment_metrics(subscription_uid=TestSparkRegressionExplainability.subscription.uid))
        print(TestSparkRegressionExplainability.ai_client.data_mart.get_deployment_metrics(asset_uid=TestSparkRegressionExplainability.subscription.source_uid))
        print(TestSparkRegressionExplainability.ai_client.data_mart.get_deployment_metrics(metric_type='quality'))

    def test_14_unsubscribe(self):
        TestSparkRegressionExplainability.ai_client.data_mart.subscriptions.delete(TestSparkRegressionExplainability.subscription.uid)

    def test_15_clean(self):
        self.wml_client.deployments.delete(TestSparkRegressionExplainability.deployment_uid)
        self.wml_client.repository.delete(TestSparkRegressionExplainability.model_uid)

    def test_16_unbind(self):
        TestSparkRegressionExplainability.ai_client.data_mart.bindings.delete(TestSparkRegressionExplainability.subscription.binding_uid)

    # def test_17_delete_data_mart(self):
    #     for uid in TestSparkRegressionExplainability.ai_client.data_mart.bindings.get_uids():
    #         TestSparkRegressionExplainability.ai_client.data_mart.bindings.delete(uid)
    #     TestSparkRegressionExplainability.ai_client.data_mart.delete()
    #     delete_schema(get_postgres_credentials(), get_schema_name())


if __name__ == '__main__':
    unittest.main()
