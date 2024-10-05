import os
import sys
import time
import logging
import traceback
from datetime import datetime, timezone
 
import schedule
from dotenv import load_dotenv

from modules.switchbot_device_collector import SwitchBotDeviceController
from modules.exceptions import *
from modules.models import SwitchbotDeviceTable, SwitchbotHubStatus, SwitchbotPlugMiniStatus, SwitchbotMeterStatus
from modules.setting import Base, Engine, session

load_dotenv()

token = os.getenv('SWITCHBOT_API_TOKEN')
secret = os.getenv('SWITCHBOT_API_SECRET_KEY')

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def device_register():
    # API call
    try:
        
        registerd_device_ids =  session.query(SwitchbotDeviceTable.device_id).all()
        registerd_device_ids = [device_id for device_id, in registerd_device_ids]

        controller = SwitchBotDeviceController(token,secret)
        result = controller.get_devices()
        device_list = result['body']['deviceList'] 

        for device in device_list:
            if device['deviceId'] not in registerd_device_ids:
                # insert
                switchbot_device = SwitchbotDeviceTable()
                switchbot_device.create_record(
                        device_id=device['deviceId'],
                        device_name=device['deviceName'],
                        device_type=device['deviceType'],
                        hub_device_id=device['hubDeviceId'],
                        enable_cloud_service=device['enableCloudService'],
                        enable_get_status=True
                )
                session.add(switchbot_device)
                logging.info(f"新しいデバイス情報 {device['deviceName']}(device id: {device['deviceId']})をセッションに追加しました")
            else:
                registerd_device = session.query(SwitchbotDeviceTable).filter(SwitchbotDeviceTable.device_id == device['deviceId']).first()
                if registerd_device.device_name != device['deviceName'] or \
                   registerd_device.hub_device_id != device['hubDeviceId'] or \
                   registerd_device.enable_cloud_service != device['enableCloudService']:
                
                    registerd_device.device_name = device['deviceName']
                    registerd_device.hub_device_id = device['hubDeviceId']
                    registerd_device.enable_cloud_service = device['enableCloudService']
                    logging.info(f"デバイスの更新情報 {device['deviceName']}(device id: {device['deviceId']})をセッションに追加しました")
                    session.add(registerd_device)

        session.commit()
        logging.info(f'セッション情報をcommitしました')

    except APIErrorExecption as e:
        logging.error(f"Error!: {str(e)}")
    except Exception as e:
        logging.error(f"Error!: {str(traceback.print_exc())}")
        session.rollback()
        logging.error(f"セッションをロールバックしました")
    finally:
        session.close()


def device_status():
    # API call
    try:
        
        registerd_device_ids =  session.query(SwitchbotDeviceTable.device_id).all()
        registerd_device_ids = [device_id for device_id, in registerd_device_ids]

        controller = SwitchBotDeviceController(token,secret)
        timestamp = datetime.now(timezone.utc)
        for device_id in registerd_device_ids:

            try:
                result = controller.get_device_status(device_id)
                is_power_on = lambda val: True if val == 'on' else False
                if result['body']['deviceType'] == 'Meter':
                    meter_status = SwitchbotMeterStatus()
                    meter_status.create_record(
                        is_api_success=True,
                        timestamp=timestamp,
                        device_id=result['body']['deviceId'],
                        humidity=result['body']['humidity'],
                        temperature=result['body']['temperature'],
                        battery=result['body']['battery'],
                        version=result['body']['version']
                    )
                    logging.info(f'こちらの情報をセッションに追加しました {result['body']}')
                    session.add(meter_status)
                elif result['body']['deviceType'] == 'Plug Mini (JP)':
                    plug_status = SwitchbotPlugMiniStatus()
                    plug_status.create_record(
                        is_api_success=True,
                        timestamp=timestamp,
                        device_id=result['body']['deviceId'],
                        voltage=result['body']['voltage'],
                        weight=result['body']['weight'],
                        electricity_of_day=result['body']['electricityOfDay'],
                        electric_current=result['body']['electricCurrent'],
                        version=result['body']['version'],
                        power=is_power_on(result['body']['power'])
                    )
                    logging.info(f'こちらの情報をセッションに追加しました {result['body']}')
                    session.add(plug_status)
                elif result['body']['deviceType'] == 'Hub 2':
                    meter_status = SwitchbotHubStatus()
                    meter_status.create_record(
                        is_api_success=True,
                        timestamp=timestamp,
                        device_id=result['body']['deviceId'],
                        humidity=result['body']['humidity'],
                        temperature=result['body']['temperature'],
                        light_level=result['body']['lightLevel'],
                        version=result['body']['version']
                    )
                    logging.info(f'こちらの情報をセッションに追加しました {result['body']}')
                    session.add(meter_status)
            except Exception as e:
                logging.error(f"Error!: {str(e)}")
                logging.error(f"Error!: {str(traceback.print_exc())}")

        session.commit()
        logging.info(f'セッション情報をcommitしました')

    except APIErrorExecption as e:
        logging.error(f"Error!: {str(e)}")
    except Exception as e:
        logging.error(f"Error!: {str(traceback.print_exc())}")
        session.rollback()
        logging.error(f"セッションをロールバックしました")
    finally:
        session.close()

if __name__ == '__main__':
    schedule.every(1).minutes.do(device_status)
    schedule.every(12).hours.do(device_register)
    while True:
        schedule.run_pending()
        time.sleep(1)