from threading import Lock

import paho.mqtt.client as mqtt


my_mutex = Lock()
mqtt_connected = False


def connect_callback_v3( connect_client: mqtt.Client, userdata, flags, connect_result_code ):
  # Paho expected signature: connect_callback_v5(client, userdata, flags, rc)
  global mqtt_connected
  mqtt_connected = True
  with my_mutex:
    print( "↑↑ ON CONNECT ↑↑" )
    print( f"  Connected client: {connect_client}" )
    print( f"  Connected with user data: '{userdata}'" )
    print( f"  Connected with flags: {flags}" )
    print( f"  Connected with reason code: {connect_result_code}" )


def disconnect_callback_v3( disconnect_client: mqtt.Client, userdata, disconnect_result_code ):
  # Paho expected signature: disconnect_callback_v5(client, userdata, rc)
  global mqtt_connected
  mqtt_connected = False
  with my_mutex:
    print( "↓↓ ON DISCONNECT ↓↓" )
    print( f"  Disconnected client: {disconnect_client}" )
    print( f"  Disconnected with user data: '{userdata}'" )
    print( f"  Disconnected with reason code: {disconnect_result_code}" )


def on_publish_callback_v3( publish_client: mqtt.Client, userdata, message_id ):
  # Paho expected signature: on_publish_callback_v5( client, userdata, mid )
  with my_mutex:
    print( "▲▲ ON PUBLISH ▲▲" )
    print( f"  Publishing client: {publish_client}" )
    print( f"  Publishing user data: '{userdata}'" )
    print( f"  Publishing message ID: {message_id}" )


def on_message_callback_v3( message_client: mqtt.Client, userdata, message ):
  # Paho expected signature: on_message_callback_v5( client, userdata, message )
  with my_mutex:
    msg = str( message.payload.decode( "utf-8" ) )
    print( "▼▼ ON MESSAGE ▼▼" )
    print( f"  Message received for client: {message_client}" )
    print( f"  Message user data: {userdata}" )
    print( f"  Message topic: {message.topic}" )
    print( f"  Message body: {msg}" )


# noinspection DuplicatedCode
def subscribe_callback_v3( subscribe_client: mqtt.Client, userdata, message_id, granted_qos ):
  # Paho expected signature: subscribe_callback_v5(client, userdata, mid, granted_qos)
  with my_mutex:
    print( "⊼⊼ ON SUBSCRIBE ⊼⊼" )
    print( f"  Subscription client: {subscribe_client}" )
    print( f"  Subscription user data: '{userdata}'" )
    print( f"  Subscription message ID: {message_id}" )
    print( f"  Subscription reason code: {granted_qos}" )


def unsubscribe_callback_v3( unsubscribe_client: mqtt.Client, userdata, message_id ):
  # Paho expected signature: unsubscribe_callback_v5(client, userdata, mid)
  with my_mutex:
    print( "⊻⊻ ON UNSUBSCRIBE ⊻⊻" )
    print( f"  Unsubscribe client: {unsubscribe_client}" )
    print( f"  Unsubscribe user data: '{userdata}'" )
    print( f"  Unsubscribe message ID: {message_id}" )
