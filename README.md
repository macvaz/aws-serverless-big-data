for i in {1..10}
do 
    curl -H "x-api-key: $API_KEY" -H 'Content-Type: application/json' -X POST -d '{"submission_id": "2", "car_brand": "Mazda"}' https://$API_GW_ID.execute-api.eu-central-1.amazonaws.com/$STAGE/Athena &
done