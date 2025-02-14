import requests
import time
import sysv_ipc
import logging
from typing import Tuple, Optional

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('gps_data.log')
    ]
)

def parse_nmea_sentence(sentence: str) -> Tuple[Optional[float], Optional[float]]:
    """
    解析 NMEA 语句，提取纬度和经度信息，并转换为十进制度。
    Args:
        sentence: NMEA格式的GPS数据字符串
    Returns:
        Tuple[Optional[float], Optional[float]]: 返回(纬度, 经度)元组，解析失败时返回(None, None)
    """
    try:
        sentence = sentence.strip()
        if not sentence:
            logging.error("收到空的NMEA语句")
            return None, None

        parts = sentence.split(',')
        if len(parts) < 6:
            logging.error(f"NMEA语句格式错误: {sentence}")
            return None, None

        # 提取经纬度信息
        lat_str, lat_dir = parts[2], parts[3]
        lon_str, lon_dir = parts[4], parts[5]

        # 验证方向指示符
        if lat_dir not in ['N', 'S'] or lon_dir not in ['E', 'W']:
            logging.error(f"无效的方向指示符: 纬度={lat_dir}, 经度={lon_dir}")
            return None, None

        # 验证经纬度字符串格式
        if not lat_str or not lon_str:
            logging.error("经纬度字符串为空")
            return None, None

        try:
            # 解析纬度
            lat_deg = float(lat_str[:2])
            lat_min = float(lat_str[2:])
            if not (0 <= lat_deg <= 90 and 0 <= lat_min < 60):
                logging.error(f"纬度值超出范围: 度={lat_deg}, 分={lat_min}")
                return None, None
            latitude = lat_deg + lat_min / 60.0
            if lat_dir == 'S':
                latitude = -latitude

            # 解析经度
            lon_deg = float(lon_str[:3])
            lon_min = float(lon_str[3:])
            if not (0 <= lon_deg <= 180 and 0 <= lon_min < 60):
                logging.error(f"经度值超出范围: 度={lon_deg}, 分={lon_min}")
                return None, None
            longitude = lon_deg + lon_min / 60.0
            if lon_dir == 'W':
                longitude = -longitude

            return latitude, longitude

        except ValueError as e:
            logging.error(f"解析经纬度数值时发生错误: {str(e)}")
            return None, None

    except (ValueError, IndexError) as e:
        logging.error(f"解析NMEA语句时发生错误: {str(e)}")
        return None, None

def send_gps_data(url: str, data: dict, max_retries: int = 3, retry_delay: float = 1.0) -> bool:
    """
    发送GPS数据到服务器，支持重试机制
    Args:
        url: 服务器URL
        data: 要发送的数据
        max_retries: 最大重试次数
        retry_delay: 重试间隔时间(秒)
    Returns:
        bool: 发送成功返回True，否则返回False
    """
    for attempt in range(max_retries):
        try:
            response = requests.post(url=url, json=data, timeout=5)
            response.raise_for_status()
            logging.info(f"数据发送成功: {data}")
            return True
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                logging.warning(f"发送失败，准备第{attempt + 2}次重试: {str(e)}")
                time.sleep(retry_delay)
            else:
                logging.error(f"发送失败，已达到最大重试次数: {str(e)}")
    return False

def main():
    flask_url = 'http://3.145.92.81:5002//data'
    key = 0x610600d7
    mem_size = 4096

    try:
        memory = sysv_ipc.SharedMemory(key, flags=sysv_ipc.IPC_CREAT, size=mem_size)
        logging.info("成功初始化共享内存")

        while True:
            try:
                memory_value = memory.read()
                memory_value = memory_value.rstrip(b'\x00')
                decoded_value = memory_value.decode('utf-8')

                lat, lon = parse_nmea_sentence(decoded_value)
                if lat is not None and lon is not None:
                    lat = round(lat, 4)
                    lon = round(lon, 4)
                    data = {
                        'car1': {
                            "latitude": lat,
                            "longitude": lon
                        }
                    }
                    send_gps_data(flask_url, data)
                time.sleep(0.5)

            except UnicodeDecodeError as e:
                logging.error(f"解码共享内存数据失败: {str(e)}")
            except Exception as e:
                logging.error(f"处理数据时发生错误: {str(e)}")
                time.sleep(1)

    except sysv_ipc.Error as e:
        logging.error(f"初始化共享内存失败: {str(e)}")
    except KeyboardInterrupt:
        logging.info("程序被用户中断")
    finally:
        try:
            memory.detach()
            memory.remove()
            logging.info("已清理共享内存资源")
        except Exception as e:
            logging.error(f"清理共享内存资源时发生错误: {str(e)}")

if __name__ == '__main__':
    main()
