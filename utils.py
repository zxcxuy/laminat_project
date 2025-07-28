import time

def wait(seconds=2):
    """Пауза в выполнении."""
    time.sleep(seconds)

floorType = ["https://premium-laminate.ru/vinilovaya_plitka"]
# floorType = ["https://premium-laminate.ru/laminat", "https://premium-laminate.ru/vinilovaya_plitka", "https://premium-laminate.ru/parketnaya_doska",
#              "https://premium-laminate.ru/ingenernaya_doska", "https://premium-laminate.ru/kovrolin", "https://premium-laminate.ru/kovrolin", 
#              "https://premium-laminate.ru/kovrovaya-plitka", "https://premium-laminate.ru/kovry", "https://premium-laminate.ru/trava",
#              "https://premium-laminate.ru/terrasnaya-doska", "https://premium-laminate.ru/wall_panels", "https://premium-laminate.ru/wall_panels",
#              "https://premium-laminate.ru/massivnaya_doska", "https://premium-laminate.ru/probkoviy_pol",
#              "https://premium-laminate.ru/flokirovannoe-pokrytie"]

db_file = "data.db"
table_names = ["Ламинат", "Кварцвиниловая плитка", "Паркетная доска", "Инженерная доска", "Ковролин",
                "Ковровая плитка", "Ковры", "Искусственная трава", "Террасная доска", "Стеновые панели",
                "Массивная доска", "Пробковый пол", "Флокированное покрытие"]