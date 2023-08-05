# goodlens_ocr_spacing

Word spacing module as OCR post correction.


------------------------------

#### Installation

Pre-requisite:
```
  proper installation of python3
  proper installation of pip

  pip install tensorflow
  pip install keras


  Windows-Ubuntu case: On following error.
  On error: /usr/lib/x86_64-linux-gnu/libstdc++.so.6: version `GLIBCXX_3.4.22' not found
     sudo apt-get install libstdc++6
     sudo add-apt-repository ppa:ubuntu-toolchain-r/test
     sudo apt-get update
     sudo apt-get upgrade
     sudo apt-get dist-upgrade (This takes long time.)
```

------------------------------

#### Usage


```
from goodlens_ocr_spacing import word_spacing

word_spacing("YOUR_TEXT_FOR_SPACING")
```