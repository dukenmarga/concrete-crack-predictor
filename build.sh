gcloud builds submit --config cloudbuild_run.yaml --project nutmeg-435109
gcloud run deploy concrete-crack-predictor --platform managed --region asia-southeast2 --image gcr.io/nutmeg-435109/concrete-crack-predictor --allow-unauthenticated --project nutmeg-435109