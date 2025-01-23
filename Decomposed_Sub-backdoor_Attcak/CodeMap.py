import base64
import datetime

Map = {}
encode_type = "map"
def encode_message(message: str) -> str:
    """对内容进行 Base64 编码或其他加密方式"""
    EncodedMessage = ""
    if encode_type == "base64":
        EncodedMessage = base64.b64encode(message.encode()).decode()
    elif encode_type == "map":
        # 自定义加密方式，采用时间对message进行加密
        # 获取当前时间的字符串格式，如 "20241106_153045"
        current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
        Map[current_time] = message
        EncodedMessage = current_time
        pass
    return EncodedMessage

def decode_message(encoded_message: str) -> str:
    """对内容进行 Base64 解码或其他解密方式"""
    DecodedMessage = ""
    if encode_type == "base64":
        DecodedMessage = base64.b64decode(encoded_message).decode()
    elif encode_type == "map":
        # 自定义解密方式，根据加密的时间戳获取message
        DecodedMessage = Map.get(encoded_message, "")
        pass
    return DecodedMessage
