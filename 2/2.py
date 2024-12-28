import json
# здесь я решаю задачу алгоритмически, не используя pymavlink

# считаем, что текущий угол дрона 90. почитал, что LiDar сканирует
# пространство на 90 гр. влево и вправо от направления

def change_direction(data):
    angles = data["angles"]
    distances = data["distances"]

    mn_i = distances.index(min(distances))  # находим минимальное расстояние
    if distances[mn_i] > 1:
        print("В радиусе 1 метра опасностей нет")
        return 0
    else:
        print(f"Объект {mn_i} находится слишком близко: {distances[mn_i]}")
        ans = 30
        if (angles[mn_i] < 90):
            ans *= -1
        print(f"Курс дрона изменён на {ans} градусов")
        return ans



input_json = '''
{
    "angles": [0, 30, 60, 90, 120, 150, 180],
    "distances": [1.2, 2.0, 3.5, 0.8, 1.1, 1.5, 2.3]
}
'''
data = json.loads(input_json)

delta = change_direction(data)

