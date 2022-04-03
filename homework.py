'''from turtle import distance'''

M_IN_KM = 1000

C_CAL_WALKING_1 = 0.035
C_CAL_WALKING_2 = 2
C_CAL_WALKING_3 = 0.029

C_CAL_SWIMING_1 = 1.1
C_CAL_SWIMING_2 = 2


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> None:
        return print(f"""
        Тип тренировки: {self.training_type};
        Длительность: {round(self.duration, 2)} ч.;
        Дистанция: {round(self.distance, 2)} км;
        Ср. скорость: {round(self.speed, 2)} км/ч;
        Потрачено ккал: {self.calories}.""")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность
                 weight: float,  # вес
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # оставляем пустым, изменяем в классе - наследнике.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        x = InfoMessage(workout_type, data[1], self.get_distance(),
                        self.get_mean_speed(), self.get_spent_calories())
        return x.get_message()


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / M_IN_KM * self.duration)


class SportsWalking(Training):
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        """Тренировка: спортивная ходьба."""
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (C_CAL_WALKING_1 * self.weight
                + (self.get_mean_speed()**C_CAL_WALKING_2 // self.height)
                * C_CAL_WALKING_3 * self.weight) * self.duration


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длинна бассейна
        self.count_pool = count_pool  # сколько раз проплыл

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self) -> float:
        """Расчет калорий."""
        return ((self.get_mean_speed() + C_CAL_SWIMING_1)
                * C_CAL_SWIMING_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Training(data[0], data[1], data[2])
    else:
        return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    'print(info.get_message())'


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
