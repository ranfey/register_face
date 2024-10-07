def get_un_sql(un):
    return "select username from user where username='" + un + "'"

def insert_user_sql(uname, pwd):
    return f"INSERT INTO user (`username`,`password`,`card_id`,`regtime`) VALUES ('{uname}','{pwd}','id_{uname}',CURRENT_TIMESTAMP())"

def get_un_with_pwd(uname, pwd):
    return "select username from administrator where username='" + uname + "' and password='" + pwd + "'"

def get_ul_sql():
    return "select a.*, b.user_user_id from user a left join access_control b on a.user_id=b.user_user_id"

def get_dev_sql():
    return "select * from device"

def get_ss_sql():
    return "select * from sensor"

def get_ss_by_d(device_id):
    return "select * from sensor where type=" + device_id

def get_dl_sql():
    return "select a.*,b.name sensor_name from tb_window a left join sensor b on a.sensor_sensor_id=b.sensor_id"

def get_dl_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from tb_window a left join sensor b on a.sensor_sensor_id=b.sensor_id where a.sensor_sensor_id=" + sensor_id

def get_tmp():
    return "select a.*,b.name sensor_name from temperature a left join sensor b on a.sensor_sensor_id=b.sensor_id"

def get_tmp_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from weather where a.sensor_sensor_id=" + sensor_id


def get_ll():
    return "select a.*,b.name sensor_name from indoor_light a left join sensor b on a.sensor_sensor_id=b.sensor_id"

def get_ll_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from indoor_light a left join sensor b on a.sensor_sensor_id=b.sensor_id where a.sensor_sensor_id=" + sensor_id


def get_door_light():
    return "select a.*,b.name sensor_name from door_light a left join sensor b on a.sensor_sensor_id=b.sensor_id"

def get_door_light_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from door_light a left join sensor b on a.sensor_sensor_id=b.sensor_id where a.sensor_sensor_id=" + sensor_id


def get_doorbell():
    return "select a.*,b.name sensor_name from doorbell a left join sensor b on a.sensor_sensor_id=b.sensor_id"


def get_doorbell_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from doorbell a left join sensor b on a.sensor_sensor_id=b.sensor_id where a.sensor_sensor_id=" + sensor_id

def get_smoke_alarm():
    return "select a.*,b.name sensor_name from smoke_alarm a left join sensor b on a.sensor_sensor_id=b.sensor_id"


def get_smoke_alarm_by_ss(sensor_id):
    return "select a.*,b.name sensor_name from smoke_alarm a left join sensor b on a.sensor_sensor_id=b.sensor_id where a.sensor_sensor_id=" + sensor_id


def get_surveillance_sql():
    return "select a.*,b.name device_name from surveillance a left join device b on a.device_device_id=b.device_id"


def get_surveillance_by_de(device_id):
    return "select a.*,b.name device_name from surveillance a left join device b on a.device_device_id=b.device_id where a.device_device_id=" + device_id


def get_access_control():
    return "select a.*,b.name device_name, c.username username from access_control a left join device b on a.device_device_id=b.device_id left join user c on a.user_user_id=c.user_id"

def get_access_control_by_de(device_id):
    return "select a.*,b.name device_name, c.username username from access_control a left join device b on a.device_device_id=b.device_id left join user c on a.user_user_id=c.user_id where a.device_device_id=" + device_id