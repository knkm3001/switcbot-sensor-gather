from datetime import date
from sqlalchemy import Column
from sqlalchemy.types import String, DateTime, Numeric, Boolean, JSON, Float
from sqlalchemy.dialects.mysql import insert, INTEGER
# sqlalchemyのデータ型については以下を参照
# https://docs.sqlalchemy.org/en/14/dialects/mysql.html?highlight=unsigned#mysql-mariadb-specific-index-options

from .setting import Base, Engine, session

class SwitchbotDeviceTable(Base):
    """
    Switchbot製品のデバイスを管理するテーブル

    Args:
        Base (DeclarativeBase): sqlalchemyの基底クラス

    Attributes:
        device_id (str)              : デバイスID (自動取得)
        device_name (str)            : デバイス名 (自動取得)
        device_type (str)            : デバイスタイプ (自動取得)
        hub_device_id  (str)         : 接続しているSwitchbotHubのデバイスID (自動取得)
        enable_cloud_service (bool)  : クラウド接続しているかどうか (自動取得)
        enable_get_status (bool) : ステータス収集APIを叩くかどうか (現状手動で更新)    
    """

    # カラム定義
    data_id                 = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    device_id               = Column(String(255), primary_key=True, nullable=False, unique=True)
    device_name             = Column(String(255), nullable=False)
    device_type             = Column(String(255), nullable=False)
    hub_device_id           = Column(String(255), nullable=False)
    enable_cloud_service    = Column(Boolean, nullable=False)
    enable_get_status   = Column(Boolean, nullable=False, default=False)

    def create_record(
            self,
            device_id,
            device_name,
            device_type,
            enable_cloud_service,
            hub_device_id=None,
            enable_get_status=False
        ):
        self.device_id = device_id
        self.device_name = device_name
        self.device_type = device_type
        self.enable_cloud_service = enable_cloud_service
        self.hub_device_id = hub_device_id
        self.enable_get_status = enable_get_status


    __tablename__ = 'switchbot_device_table' # テーブル名
    __table_args__ = {'extend_existing': True,"mysql_charset": "utf8mb4"} # テーブル定義時に実行で再定義可



class SwitchbotHubStatus(Base):
    """
    Swhitchbot Hubから取得したデータ

    Args:
        Base (DeclarativeBase): sqlalchemyの基底クラス

    Attributes:
        record_id (int)         : レコードID
        is_api_success (bool)   : API取得時に接続成功したか
        timestamp (datetime)    : データ送信日時
        device_id (str)         : デバイスID
        hub_device_id (str)     : ハブのデバイスID
        humidity (int)          : 湿度[%]
        temperature (float)     : 温度[℃]
        light_level (int)       : 照度 1~20段階
        version (str)           : ファームウェアバージョン 
    """

    __tablename__ = 'switchbot_hub_status' # テーブル名
    __table_args__ = {'extend_existing': True,"mysql_charset": "utf8mb4"} # テーブル定義時に実行で再定義可


    # カラム定義
    record_id       = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    is_api_success  = Column(Boolean, nullable=False)
    timestamp       = Column(DateTime, nullable=False)
    device_id       = Column(String(255), nullable=False)
    humidity        = Column(INTEGER)
    temperature     = Column(Float)
    light_level     = Column(INTEGER)
    version         = Column(String(255))

    def create_record(
            self,
            is_api_success,
            timestamp,
            device_id,
            humidity=None,
            temperature=None,
            light_level=None,
            version=None
        ):
        self.is_api_success = is_api_success
        self.timestamp = timestamp
        self.device_id = device_id
        self.humidity = humidity
        self.temperature = temperature
        self.light_level = light_level
        self.version = version



class SwitchbotPlugMiniStatus(Base):
    """
    Swhitchbot Plug Mini(JP)から取得したデータ

    Args:
        Base (DeclarativeBase): sqlalchemyの基底クラス

    Attributes:
        record_id (int)              : レコードID (PK)
        is_api_success (bool)       : API取得時に接続成功したか
        timestamp (datetime)        : データ送信日時
        device_id (str)             : デバイスID
        voltage (float)             : 電圧[V]
        weight (float)              : 一日あたりの消費電力[W]
        electricity_of_day (float)  : 一日あたりの使用時間[min]
        electric_current (float)    : 現在の消費電流[A] 
        power (str)                 : 現在の使用状態 on/off
        version (str)               : ファームウェアバージョン 
    """
  
    __tablename__ = 'switchbot_plug_mini_status' # テーブル名
    __table_args__ = {'extend_existing': True,"mysql_charset": "utf8mb4"} # テーブル定義時に実行で再定義可

    # カラム名
    record_id          = Column(INTEGER(unsigned=True), nullable=False, autoincrement=True, primary_key=True) 
    is_api_success     = Column(Boolean, nullable=False)
    timestamp          = Column(DateTime, nullable=False)
    device_id          = Column(String(255), nullable=False)
    voltage            = Column(Float)
    version            = Column(String(255))
    weight             = Column(Float)
    electricity_of_day = Column(Float)
    electric_current   = Column(Float)
    power              = Column(Boolean)

    def create_record(
            self,
            is_api_success,
            timestamp,
            device_id,
            voltage=None,
            version=None,
            weight=None,
            electricity_of_day=None,
            electric_current=None,
            power=None
        ):
        self.is_api_success = is_api_success
        self.timestamp = timestamp
        self.device_id = device_id
        self.voltage = voltage
        self.version = version
        self.weight = weight
        self.electricity_of_day = electricity_of_day
        self.electric_current = electric_current
        self.power = power


class SwitchbotMeterStatus(Base):
    """
    Swhitchbot Meterから取得したデータ

    Args:
        Base (DeclarativeBase): sqlalchemyの基底クラス

    Attributes:
        record_id (int)         : レコードID (PK)
        is_api_success (bool)   : API取得時に接続成功したか
        timestamp (datetime)    : データ送信日時
        device_id (str)         : デバイスID
        hub_device_id (str)     : ハブのデバイスID
        humidity (int)          : 湿度[%]
        temperature (float)     : 温度[℃] 
        version (str)           : ファームウェアバージョン 
        battery (int)           : バッテリー状態
    """

    __tablename__ = 'switchbot_meter_status' # テーブル名
    __table_args__ = {'extend_existing': True,"mysql_charset": "utf8mb4"} # テーブル定義時に実行で再定義可


    # カラム定義
    record_id       = Column(INTEGER(unsigned=True), primary_key=True, autoincrement=True, nullable=False)
    is_api_success  = Column(Boolean, nullable=False)
    timestamp       = Column(DateTime, nullable=False)
    device_id       = Column(String(255), nullable=False)
    humidity        = Column(INTEGER)
    temperature     = Column(Float)
    version         = Column(String(255))
    battery         = Column(INTEGER)

    def create_record(
            self,
            is_api_success,
            timestamp,
            device_id,
            humidity=None,
            temperature=None,
            version=None,
            battery=None
        ):
        self.is_api_success = is_api_success
        self.timestamp = timestamp
        self.device_id = device_id
        self.humidity = humidity
        self.temperature = temperature
        self.version = version
        self.battery = battery

if __name__ == '__main__':
    try:
        print('create tables start')
        Base.metadata.create_all(bind=Engine)
    except:
        print('exception occur')
        session.rollback()
        raise
    finally:
        print('fin')
        session.close()