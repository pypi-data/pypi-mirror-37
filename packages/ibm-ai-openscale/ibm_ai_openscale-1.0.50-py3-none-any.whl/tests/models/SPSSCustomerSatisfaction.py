import os


def get_model_data():
    file_path = os.path.join(os.getcwd(), 'artifacts', 'SPSSCustomerSatisfaction',
                             'customer-satisfaction-prediction.str')

    return {
        'path': file_path
    }


def get_scoring_payload():
    return {
        "fields": [
            "customerID",
            "gender",
            "SeniorCitizen",
            "Partner",
            "Dependents",
            "tenure",
            "PhoneService",
            "MultipleLines",
            "InternetService",
            "OnlineSecurity",
            "OnlineBackup",
            "DeviceProtection",
            "TechSupport",
            "StreamingTV",
            "StreamingMovies",
            "Contract",
            "PaperlessBilling",
            "PaymentMethod",
            "MonthlyCharges",
            "TotalCharges",
            "Churn",
            "SampleWeight"
        ],
        "values": [
            [
                "3638-WEABW",
                "Female",
                0,
                "Yes",
                "No",
                58,
                "Yes",
                "Yes",
                "DSL",
                "No",
                "Yes",
                "No",
                "Yes",
                "No",
                "No",
                "Two year",
                "Yes",
                "Credit card (automatic)",
                59.9,
                3505.1,
                "No",
                2.768
            ]
        ]
    }
