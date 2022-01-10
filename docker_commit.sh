#!/bin/sh0
COMMENT=$1
VERSION=$2

export api_image_id=$(docker container ls  | grep 'pingo_daphne' | awk '{print $1}')

echo "Commit and push ${api_image_id} lionhu/wavus_pingo:v_${VERSION}"
docker commit -a "lionhu" -m "$COMMENT"    $api_image_id "lionhu/wavus_pingo:v_${VERSION}"
docker push "lionhu/wavus_pingo:v_${VERSION}"


export api_image_id=$(docker container ls  | grep 'celery' | awk '{print $1}')

echo "Commit and push ${api_image_id} lionhu/wavus_pingo_celery:v_${VERSION}"
docker commit -a "lionhu" -m "$COMMENT"    $api_image_id "lionhu/wavus_pingo_celery:v_${VERSION}"
docker push "lionhu/wavus_pingo_celery:v_${VERSION}"

echo "=========COMPLETED=========="
