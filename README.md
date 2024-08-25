Bước 1:install python 3.8

https://www.python.org/downloads/release/python-3810/
chọn phiên bản và cài
=> nhớ tích vào thêm environment biến trong khi cài đặt


Bước 2: down chromedriver để điều khiển web
check phiên bản chrome hiện tại:
vào chrome gõ : chrome://version/ => DÒNG ĐẦU TIÊN CHO THẤY PHIÊN BẢN CHROME HIỆN TẠI

Giả sử là : 127.0.6533.120

Thì thay phiên bản vào đường dẫn sau:

- Đối với window:

https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.120/win64/chromedriver-win64.zip
pip install selenium

- đối với Linux:
https://storage.googleapis.com/chrome-for-testing-public/127.0.6533.120/linux64/chromedriver-linux64.zip


Giải nén file zip vừa down

Bước 3: Download code
https://github.com/linhbktb/tekika 
Có thể dùng git clone hoặc download zip

Bước 4: copy file chromedriver(linux) hoặc chromedriver.exe(window) (download ở bước 2) vào cùng thư mục code (download ở bước 3)

Bước 5: cd vào thư mục code và run câu lệnh sau

python autoCoin.py (win)

hoặc

python3 autoCoin.py (linux)
