if [ "$#" -eq 0 ] ;
  then echo "No agruments supplied"
  exit -1
fi

echo $1 > /sys/class/drm/card0/device/hwmon/hwmon0/pwm1
echo $1 > /sys/class/drm/card1/device/hwmon/hwmon1/pwm1

echo Set fan speeds to $1
