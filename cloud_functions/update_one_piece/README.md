# Cloud Function to update the cards database

## Deploy
```
gcloud functions deploy update-onepiece-sets \
   --region=europe-west9 \
   --runtime=python312 \
   --source=. \
   --entry-point=main \
   --trigger-http
```