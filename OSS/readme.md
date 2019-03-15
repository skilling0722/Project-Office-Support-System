Office Support System(OSS)
***

What?:
***
OSS Provides a variety of functions for collaboration.

Function: memo&alarm, login, file, weather, chat

Environment:
***
    window 7 or more
    ubuntu 16.04 or 18.04
    pymysql
    PyQt5 
    ftp
    pygame
    smtplib
    OWM API
    Papago NMT API
    Mysql DB
    AWS EC2 server

composition:
***
    hom.py

    main dir - main_ui.py, main_widget.py, popup.py

    chat dir - chat_widget.py, ex_client.py

    file dir - file_widget.py, delete_file.py, download_file.py, upload_file.py, rename_file.py, rename_input.py, file_db.py, ftp dir - ftp_delete.py, ftp.download.py, ftp_rename.py, ftp_upload.py

    member dir - member_widget.py, DB_info.py, member_join.py, member_search.py, member_search_id.py, member_search_pwd.py, member_update_pwd.py, generate_certify_code.py, certification.py, User_info.py, OSS_smtp.py

    memo dir - memo_widget.py, memo_db.py, general_memo.py, alarm_memo.py, view_memo.py, view_alarm_memo.py, time_input.py

    weather dir - weather_widget.py, weather_py, input_locate.py

    img dir - GUI img

    sound dir - alarm sound

Run:
***
    python hom.py

Caution:
***
This program works in conjunction with the server and database, so it is not available when the required server and database are not in operation.

Example:
***
Function
![function](https://user-images.githubusercontent.com/41464934/54429692-8e3a5500-4764-11e9-9cd0-18cdbed62ce7.JPG)
***

Achitecture
![Achitecture](https://user-images.githubusercontent.com/41464934/54429694-8ed2eb80-4764-11e9-9685-20bd6ad26d9a.JPG)
***
Login screen
![login](https://user-images.githubusercontent.com/41464934/54429687-8da1be80-4764-11e9-840e-1d3816594e6d.PNG)
***
Initial screen
![init](https://user-images.githubusercontent.com/41464934/54429690-8e3a5500-4764-11e9-8cbe-6620ec77e211.PNG)
***
File screen
![file](https://user-images.githubusercontent.com/41464934/54429689-8da1be80-4764-11e9-89f3-5c3de45b605d.PNG)
***
Memo screen
![memo](https://user-images.githubusercontent.com/41464934/54429688-8da1be80-4764-11e9-83ce-9caa451e4b75.PNG)
***
Weather screen
![weather](https://user-images.githubusercontent.com/41464934/54429691-8e3a5500-4764-11e9-9e36-1c23a804dce6.PNG)



