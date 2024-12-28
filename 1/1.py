from pymavlink import mavutil

the_connection = mavutil.mavlink_connection('udpin:localhost:14551')
# здесь нужно указать ip-адрес и порт дрона
# есть симка (на собесе уточнили), значит, и доступ в интернет есть

# дожидаемся соединения
the_connection.wait_heartbeat()
print(f"Получен heartbeat от {the_connection.target_system}, компонент {the_connection.target_component}")

msg = the_connection.recv_match(type="COMMAND_ACK", blocking=True)
if (msg.result != 0):
    print("не удалось подключиться. завершение скрипта")
    exit(1)
else:
    print(f"подключено успешно: {msg}")

# эта команда приводит дрон в позицию готовности, как я понял. в туториале было
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 1, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type="COMMAND_ACK", blocking=True)
if (msg.result != 0):
    print("не удалось привести дрон в готовность. завершение скрипта")
    exit(1)
else:
    print(f"дрон готов к задачам: {msg}")

# взлёт
altitude = 10  # высота полёта
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, altitude)

msg = the_connection.recv_match(type="COMMAND_ACK", blocking=True)
if (msg.result != 0):
    print("не взлетели. завершение скрипта")
    exit(1)
else:
    print(f"взлёт совершён: {msg}")

# передаём координаты маршрута
positions = [[0, 10, altitude],
             [10, 10, altitude],
             [10, 0, altitude],
             [0, 0, altitude]]

for seq, position in enumerate(positions):
    lat, lon, alt = position

    the_connection.mav.mission_item_int_send(the_connection.target_system, the_connection.target_component, seq,
                                             mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
                                             mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
                                             0, 1 if seq < len(positions) - 1 else 0, #это для автопродления, поле autocontinue
                                             0, 0, 0, 0,
                                             int(lat * 1e7), int(lon * 1e7), alt, 0)

    msg = the_connection.recv_match(type="MISSION_ACK", blocking=True)
    if (msg.result != 0):
        print(f"позиция {seq} не передана. завершение скрипта")
        exit(1)

print(f"позиции задания переданы")

# запускаем миссию - облёт всех точек маршрута
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_MISSION_START, 0, 0, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type="COMMAND_ACK", blocking=True)
if (msg.result != 0):
    print("миссия не началась. завершение скрипта")
    exit(1)
else:
    print(f"миссия началась: {msg}")

# тут нужно написать скрипт, который дожидается конца миссии. наверно, просто
# судит по координатам, долетел ли дрон до конца маршрута или нет

# приземляемся
the_connection.mav.command_long_send(the_connection.target_system, the_connection.target_component,
                                     mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0)

msg = the_connection.recv_match(type="COMMAND_ACK", blocking=True)
if (msg.result != 0):
    print("посадка не завершена. завершение скрипта")
    exit(1)
else:
    print(f"посадка совершена: {msg}")
