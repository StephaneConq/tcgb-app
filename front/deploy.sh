export PROJECT="tcgb-app"
export APP_NAME="tcgb"

docker build -t europe-west9-docker.pkg.dev/${PROJECT}/${APP_NAME}-repo/${APP_NAME}-front:latest .

docker push europe-west9-docker.pkg.dev/${PROJECT}/${APP_NAME}-repo/${APP_NAME}-front:latest

gcloud builds submit --tag europe-west9-docker.pkg.dev/${PROJECT}/${APP_NAME}-repo/${APP_NAME}-front:latest

gcloud run deploy ${APP_NAME}-front --image europe-west9-docker.pkg.dev/${PROJECT}/${APP_NAME}-repo/${APP_NAME}-front:latest --platform managed --region europe-west9