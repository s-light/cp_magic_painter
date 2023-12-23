# Py QT esp32-s3 board setup

```bash
cd /circuitpython/tinyuf2-adafruit_qtpy_esp32s3-0.16.0
$ rsync esptool.py --port /dev/ttyACM0 write_flash 0x0 combined.bin 
esptool.py v4.6.2
Serial port /dev/ttyACM0
Connecting...
Detecting chip type... ESP32-S3
Chip is ESP32-S3 (revision v0.1)
Features: WiFi, BLE
Crystal is 40MHz
MAC: f4:12:fa:8d:98:88
Uploading stub...
Running stub...
Stub running...
Configuring flash size...
Flash will be erased from 0x00000000 to 0x0043afff...
Compressed 4433760 bytes to 131067...
Wrote 4433760 bytes (131067 compressed) at 0x00000000 in 12.5 seconds (effective 2834.0 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
$ 
$ rsync -r --info=progress2 --info=name0  ../adafruit-circuitpython-adafruit_qtpy_esp32s3_nopsram-en_GB-8.2.6.uf2 /media/$USER/QTPYS3BOOT/
      2.809.856 100%  313,56kB/s    0:00:08 (xfr#1, to-chk=0/1)
$ rsync rsync -r --info=progress2 --info=name0 --exclude '/tests' ~/mydata/github/cp_magic_painter/fw/* /media/$USER/CIRCUITPY/
rsync: [Receiver] mkdir "/media/$USER/CIRCUITPY" failed: Permission denied (13)
rsync error: error in file IO (code 11) at main.c(791) [Receiver=3.2.7]
$ rsync -r --info=progress2 --info=name0 --exclude '/tests' ~/mydata/github/cp_magic_painter/fw/* /media/$USER/CIRCUITPY/
rsync: [Receiver] change_dir#1 "/media/$USER/CIRCUITPY/" failed: Permission denied (13)
rsync error: errors selecting input/output files, dirs (code 3) at main.c(751) [Receiver=3.2.7]
$ rsync -r --info=progress2 --info=name0 --exclude '/tests' ~/mydata/github/cp_magic_painter/fw/* /media/$USER/CIRCUITPY/
        176.743 100%   12,28kB/s    0:00:13 (xfr#56, to-chk=0/67) 
$ rsync rm /media/$USER/CIRCUITPY/code.py 
$ sync
$ 
```