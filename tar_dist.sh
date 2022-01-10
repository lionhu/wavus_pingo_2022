#!/bin/sh


echo ">>>>>Tar dist folder for front and backend app<<<<<"

set -e
PWD=`pwd`
TARGET_PATH="`pwd`/dist_packages"

FRONT_PATH="`pwd`/front_app"
FRONT_DIST_PATH="dist"
FRONT_TARFILE="front_dist.tar.gz"

BACK_PATH="`pwd`/backend_app"
BACK_DIST_PATH="dist"
BACK_TARFILE="backend_dist.tar.gz"


if [ -d $TARGET_PATH ]; then
  echo "dist_packages exists, deleted it!"
   rm -rf  $TARGET_PATH
fi

mkdir $TARGET_PATH

#(
#  docker exec nuxtjs_app npm run generate
#  docker exec backend_app npm run generate
#  exit 0
#) &
#  PID_0=$!
#
#  wait $PID_0; echo "$FRONT_TARFILE finished."


(
  cd $FRONT_PATH
  npm run generate
) &

(
  cd $BACK_PATH
  npm run generate
) &
  wait; echo "generated dist for front and back"


(
  cd $FRONT_PATH
  if [ -f "$FRONT_TARFILE" ]; then
      rm "$FRONT_TARFILE"
      echo "$FRONT_TARFILE exists and has been removed."
  fi
  echo "Compressing $FRONT_TARFILE..."
  tar -czf  $FRONT_TARFILE $FRONT_DIST_PATH


  exit 0
) &
  PID_0=$!

  wait $PID_0; echo "$FRONT_TARFILE finished."


(

  cd $BACK_PATH
  if [ -f "$BACK_TARFILE" ]; then
      rm "$BACK_TARFILE"
      echo "$BACK_TARFILE exists and has been removed."
  fi
  echo "Compressing $FRONT_TARFILE..."
  tar -czf $BACK_TARFILE $BACK_DIST_PATH

  exit 0
) &
  PID_1=$!

  wait $PID_1; echo "$BACK_TARFILE finished."


  mv "$FRONT_PATH/$FRONT_TARFILE" $TARGET_PATH
  echo "move $FRONT_TARFILE to $TARGET_PATH"
  mv "$BACK_PATH/$BACK_TARFILE" $TARGET_PATH
  echo "move $BACK_TARFILE to $TARGET_PATH"

echo ">>>>>----- COMPLETED -----<<<<<"
