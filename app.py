import os
from datetime import datetime, timedelta
import base64
import time
import cv2 as cv
import numpy as np
import face_recognition
from flask import *
import pymysql

from db import selectSql, execSql, getDb
from get_sql import (
    get_un_sql,
    insert_user_sql,
    get_un_with_pwd,
    get_ul_sql,
    get_dev_sql,
    get_ss_sql,
    get_ss_by_d,
    get_dl_sql,
    get_dl_by_ss,
    get_tmp,
    get_tmp_by_ss,
    get_ll,
    get_ll_by_ss,
    get_door_light,
    get_door_light_by_ss,
    get_doorbell,
    get_doorbell_by_ss,
    get_smoke_alarm,
    get_smoke_alarm_by_ss,
    get_surveillance_sql,
    get_surveillance_by_de,
    get_access_control,
    get_access_control_by_de,
)


app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(24)  # 设置密钥
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)  # 配置7天有效

UPLOAD_FOLDER = "static/uploads"


# 图像解码函数
def decode_image(img_data):
    if img_data.startswith("data:image"):
        img_str = img_data.split(",")[1]
    else:
        img_str = img_data

    img_bytes = base64.b64decode(img_str)
    np_arr = np.frombuffer(img_bytes, np.uint8)
    img = cv.imdecode(np_arr, cv.IMREAD_COLOR)
    if img is None:
        print("图像解码失败")
    return img


# 查询人脸是否存在
def face_exists(encoding_str, tolerance=0.5):
    conn = getDb()
    cursor = conn.cursor()

    # 查找数据库中的所有人脸编码
    query_sql = "SELECT user_id, user_name, picture FROM xxq.user"
    cursor.execute(query_sql)
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    if not results:
        return {"exists": False}

    # 将当前人脸编码转换为 numpy 数组
    current_encoding = np.array(list(map(float, encoding_str.split(","))))

    # 遍历数据库中的每一条记录，进行对比
    for user_id, user_name, db_encoding_str in results:
        db_encoding = np.array(list(map(float, db_encoding_str.split(","))))

        # 计算两者的欧式距离
        distance = np.linalg.norm(db_encoding - current_encoding)

        if distance <= tolerance:
            return {"exists": True, "user_id": user_id, "user_name": user_name}

    # 如果没有匹配
    return {"exists": False}


# 保存图像到指定目录，以 user_name 命名文件
def save_image(img_data, face_location, user_name):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{user_name}_{timestamp}.jpg"
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    left, top, width, height = face_location
    cropped_face = img_data[top : top + height, left : left + width]

    cv.imwrite(file_path, cropped_face)
    return file_path


# 检测人脸并进行处理
@app.route("/detect_face", methods=["POST"])
def detect_face():
    data = request.get_json()
    img_data = data["image"]

    # 解码图像
    img = decode_image(img_data)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    # 检测人脸
    face_locations = face_recognition.face_locations(img_rgb)
    if len(face_locations) == 0:
        return jsonify({"detected": False})

    current_user = {"user_id": 1, "user_name": "test"}

    user_name = current_user.get("user_name")

    # 提取人脸编码
    face_encoding = face_recognition.face_encodings(img_rgb, face_locations)[0]
    encoding_str = ",".join(map(str, face_encoding.tolist()))

    # 检查是否存在
    result = face_exists(encoding_str)

    # 获取第一个人脸的位置
    top, right, bottom, left = face_locations[0]
    face_location = [left, top, right - left, bottom - top]

    if result["exists"]:
        # 返回匹配到的用户信息
        return jsonify(
            {
                "detected": True,
                "exists": True,
                "user_name": result["user_name"],
                "face_location": face_location,
            }
        )
    else:
        # 保存人脸图像
        file_path = save_image(img, face_location, user_name)
        return jsonify(
            {
                "detected": True,
                "exists": False,
                "face_location": face_location,
                "saved_image": file_path,
            }
        )


# 录入人脸
@app.route("/register_face", methods=["POST"])
def register_face():
    data = request.get_json()
    img_data = data["image"]
    img = decode_image(img_data)
    img_rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    user_id = data["user_id"]
    user_name = data["user_name"]
    # 提取人脸编码
    face_encoding = face_recognition.face_encodings(img_rgb)[0]
    encoding_str = ",".join(map(str, face_encoding.tolist()))

    # 将人脸编码存入数据库
    conn = getDb()
    cursor = conn.cursor()
    insert_sql = "INSERT INTO xxq.user(user_id, user_name, picture) VALUES(%s, %s, %s)"
    cursor.execute(insert_sql, (user_id, user_name, encoding_str))
    conn.commit()
    cursor.close()
    conn.close()

    return jsonify({"success": True})


# 删除用户人脸数据的路由
@app.route("/delete_face", methods=["POST"])
def delete_face():
    data = request.get_json()

    # 获取要删除的用户名
    user_name = data.get("user_name")

    if not user_name:
        return jsonify({"error": "缺少用户名"}), 400

    # 从数据库中删除该用户的人脸记录
    conn = getDb()
    cursor = conn.cursor()

    # 删除语句
    delete_sql = "DELETE FROM xxq.user WHERE user_name = %s"
    cursor.execute(delete_sql, (user_name,))

    # 提交更改并关闭连接
    conn.commit()
    cursor.close()
    conn.close()

    return (
        jsonify({"success": True, "message": f"用户 {user_name} 的人脸数据已删除"}),
        200,
    )


@app.route("/")
def face():
    return render_template("faces.html")


import torch

model = torch.hub.load(
    "C:\\yolo\\yolov5", "custom", path="C:\\yolo\\yolov5\\best.pt", source="local"
)
# yolo加载模型


@app.route("/detect_object", methods=["POST"])
def detect_object():
    data = request.get_json()
    img_data = data["image"]

    # 解码图像
    img = decode_image(img_data)

    # 创建两个文件夹用于保存图片
    before_folder = "./uploads/img/before"
    after_folder = "./uploads/img/after"
    os.makedirs(before_folder, exist_ok=True)
    os.makedirs(after_folder, exist_ok=True)

    results = model(img)

    detected_objects = []
    if len(results.xyxy[0]) > 0:
        before_image_path = os.path.join(before_folder, f"{time.time()}_original.jpg")
        cv.imwrite(before_image_path, img)

        processed_image_path = os.path.join(
            after_folder, f"{time.time()}_processed.jpg"
        )

        for obj in results.xyxy[0]:  # 遍历每个检测结果
            x1, y1, x2, y2, conf, cls = obj[:6]
            label = results.names[int(cls)]  # 获取物体标签
            detected_objects.append(
                {
                    "label": label,
                    "coordinates": [
                        int(x1),
                        int(y1),
                        int(x2),
                        int(y2),
                    ],  # 坐标：左上角和右下角
                    "confidence": float(conf),  # 置信度
                }
            )

            # 在图像上画检测框和标签
            cv.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            cv.putText(
                img,
                f"{label} {conf:.2f}",
                (int(x1), int(y1) - 10),
                cv.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 255, 0),
                2,
            )

        # 保存处理后的图片到 "after" 文件夹
        cv.imwrite(processed_image_path, img)

        # 将原始图片和处理后的图片路径存入数据库
        save_path(before_image_path, processed_image_path)
    else:
        print("No objects detected, not saving any images or database entry.")

    return jsonify({"detected": len(detected_objects) > 0, "objects": detected_objects})


def save_path(before_path, after_path):
    insert_sql = "INSERT INTO xxq.yolo (record_time, before_picture, after_picture) VALUES (%s, %s, %s)"
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    formatted_sql = insert_sql % (f"'{now}'", f"'{before_path}'", f"'{after_path}'")

    try:
        result = execSql(formatted_sql)
        if result > 0:
            print(f"Data saved to database: {before_path}, {after_path}")
        else:
            print("Data insert failed.")
    except Exception as e:
        print(f"Database Error: {e}")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5968)
