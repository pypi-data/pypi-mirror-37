# <h2 id="title"> Thư viên Schedule trên ngôn ngữ Python để chạy service background.</h2>

# Copyright: MobioVN

# <h2 id="version">Version</h2>
Phiên bản hiện tại `0.2`

# Cài đặt:
`pip3 install m-schedule`

# Sử dụng:
```
class TestScheduler(BaseScheduler):
    def __init__(self):
        # do something

    def owner_do(self):
        # TODO

    def get_schedule(self):
        """
        hàm xác định thời điểm chạy của scheduler, bằng cách xử dụng thư viện schedule
        Các ví dụ hướng dẫn cách xác định thời gian chạy
        1. scheduler chỉ thực hiện công việc một lần duy nhất.
            return None
        2. scheduler sẽ thực hiện mỗi 10 phút một lần.
            return schedule.every(10).minutes
        3. scheduler sẽ thực hiện hàng ngày vào lúc 10h 30 phút.
            return schedule.every().day.at("10:30")
        4. scheduler sẽ thực hiện sau mỗi giờ.
            return schedule.every().hour
        5. scheduler sẽ thực hiện vào mỗi thứ 2 hàng tuần.
            return schedule.every().monday
        6. scheduler sẽ thực hiện vào mỗi thứ 5 hàng tuần và vào lúc 13h 15'.
            return schedule.every().wednesday.at("13:15")
        """
    return schedule.every(10).minutes
```

# Build & distribute new version
## <h2 id="prepare">Prepare</h2>
1. Tạo tài khoản tại site: [https://test.pypi.org](https://test.pypi.org)
2. Tạo tài khoản tại site: [https://pypi.org/](https://pypi.org)

## <h2 id="build">Build</h2>
Make sure you have the latest versions of setuptools and wheel installed:

`python3 -m pip install --user --upgrade setuptools wheel`

Now run this command from the same directory where setup.py is located:

`python3 setup.py sdist bdist_wheel`

## <h2 id="upload">Uploading the distribution archives</h2>
Now that you are registered, you can use [twine](https://packaging.python.org/key_projects/#twine) to upload the distribution packages. You’ll need to install Twine:

`python3 -m pip install --user --upgrade twine`

Once installed, run Twine to upload all of the archives under dist:

`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`

Upload to PyPI

`twine upload dist/*`