#-- Version: 0.0.1
#-- Example script on how to use ai api client
import time
from datetime import datetime
from clarivate import aiapi
from clarivate.aiapi import config


def example_use_of_aiapi_client():
    start = time.time()
    now = datetime.now()
    print('Process started at %s....' %(now))

    # define API_KEY in config.py or simply pass the apikey in the class augument
    print(config.API_KEY, config.SERVER_URL)
    client = aiapi.Client(config.API_KEY, config.SERVER_URL)

    response_data1, _ = client.info('dealspa')
    response_data2, _ = client.ontologies('dealspa')
    response_data3, _ = client.ontology('dealspa', 'companyName', 'cancer')
    response_data4, _ = client.predictions()
    response_data5, _ = client.predictions('dealspa')

    # prediction inputs
    inputs = {
        "model": "deals-pa-01",
        "inputs": [
        {
            "field": "therapyArea",
            "op": "eq",
            "value": "3"
        },
        {
            "field": "indication",
            "op": "eq",
            "value": "49"
        },        
        {
            "field": "partnerCompanyType",
            "op": "eq",
            "value": "4"
        }
    ]
    }
    response_data6, process_logs = client.predict('dealValueSuccessPredictionsDrug', inputs)

    print(response_data1)
    # {'name': 'Deals Predictive Analytics', 'description': 'Predict deal value and clinical success with statistical model.\n
    # Cortellis Deals Intelligence™ applies data science techniques, including a combination of automated machine learning and human intelligence,
    # to 20 years of historic deals intelligence to help you accurately predict deal valuation and probability of success for partnered assets.\n
    # A proprietary, predictive analytics algorithm draws on more than 20 traits from across the entire body of Cortellis data for a statistical model
    # that calculates success after licensing and target valuation for each asset type for an individual drug class.'}
    print("============")
    print(response_data2)
    # {
    # "status":"success",
    # "data":[
    #     {
    #         "name":"therapyArea",
    #         "list":true
    #     },
    #     {
    #         "name":"indication",
    #         "list":true
    #     },
    #     {
    #         "name":"dealType",
    #         "list":true
    #     },
    #     {
    #         "name":"entityType",
    #         "list":true
    #     },
    #     {
    #         "name":"technology",
    #         "list":true
    #     },
    #     {
    #         "name":"companyType",
    #         "list":true
    #     },
    #     {
    #         "name":"companyName",
    #         "list":false
    #     }
    #     ]
    # }
    print("============")
    print(response_data3)
    # {
    #     "status":"success",
    #     "data":[
    #         {
    #             "company_id":"1005775",
    #             "company_type_id":"1",
    #             "company_name":"National Cancer Center of Korea",
    #             "status":"Active"
    #         },
    #         {
    #             "company_id":"1007673",
    #             "company_type_id":"1",
    #             "company_name":"Centenary Institute Cancer Medicine & Cell Biology",
    #             "status":"Active"
    #         },
    #         {
    #             "company_id":"1007766",
    #             "company_type_id":"1",
    #             "company_name":"BC Cancer Agency",
    #             "status":"Active"
    #         },
    #         ...
    #     ]
    # }
    print("============")
    print(response_data4)
    # {
    #     "status":"success",
    #     "data":[
    #         {
    #             "name":"dealValueSuccessPredictionsDrug"
    #         },
    #         {
    #             "name":"dealValueSuccessPredictionsFunding"
    #         },
    #         {
    #             "name":"dealValueSuccessPredictionsTechnology"
    #         }
    #     ]
    # }
    print("============")
    print(response_data5)
    # {
    #     "status":"success",
    #     "data":[
    #         {
    #             "name":"dealValueSuccessPredictionsDrug"
    #         },
    #         {
    #             "name":"dealValueSuccessPredictionsFunding"
    #         },
    #         {
    #             "name":"dealValueSuccessPredictionsTechnology"
    #         }
    #     ]
    # }
    print("============")
    print(response_data6)
    # {
    #     "status":"success",
    #     "data":[
    #         {
    #             "success":{
    #                 "long_term":"0.41",
    #                 "short_term":"0.24"
    #             },
    #             "value":{
    #                 "upfront":"8.51",
    #                 "total_paid":"33.43",
    #                 "total_at_signing":"78.41"
    #             },
    #             "phase_name":"Discovery"
    #         },
    #         {
    #             "success":{
    #                 "long_term":"0.53",
    #                 "short_term":"0.34"
    #             },
    #             "value":{
    #                 "upfront":"12.74",
    #                 "total_paid":"52.73",
    #                 "total_at_signing":"128.57"
    #             },
    #             "phase_name":"Phase 1"
    #         },
    #         ...
    #     ]
    # }
    print("============")
    print('\n'.join('{}\t{}'.format(x[0],x[1]) for x in process_logs))
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/info/dealspa
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/ontology/dealspa
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/ontology/dealspa/companyName?search=cancer
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/prediction
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/prediction?contentset=dealspa
    # SUCCESS successfully receive response from endpoint http://api.dev-snapshot.clarivate.com/c3/ai/prediction/dealValueSuccessPredictionsDrug
    elapsed = (time.time() - start)/60
    print('Process completed! time taken: %s minutes' %(str(elapsed)))

if __name__ == "__main__":
        example_use_of_aiapi_client()