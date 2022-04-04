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

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность
                 weight: float,  # вес
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = ''

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # оставляем пустым, изменяем в классе - наследнике.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        self.training_type = 'Running'
        self.c_time = 60

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        coeff_calorie_1 = 18
        coeff_calorie_2 = 20
        return ((coeff_calorie_1 * self.get_mean_speed() - coeff_calorie_2)
                * self.weight / self.M_IN_KM * (self.duration * self.c_time))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.training_type = 'SportsWalking'
        self.C_CAL_WALKING_1 = 0.035
        self.C_CAL_WALKING_2 = 2
        self.C_CAL_WALKING_3 = 0.029
        self.c_time = 60

    def get_spent_calories(self) -> float:
        return (self.C_CAL_WALKING_1 * self.weight
                + (self.get_mean_speed()**self.C_CAL_WALKING_2 // self.height)
                * self.C_CAL_WALKING_3 * self.weight) * (self.duration * self.c_time)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    C_CAL_SWIMING_1 = 1.1
    C_CAL_SWIMING_2 = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # длинна бассейна
        self.count_pool = count_pool  # сколько раз проплыл
        self.training_type = 'Swimming'

#    def get_distance(self) -> float:
#        """Получить дистанцию в км."""
#        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Расчет калорий."""
        return ((self.get_mean_speed() + self.C_CAL_SWIMING_1)
                * self.C_CAL_SWIMING_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type == 'SWM':
        return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
        return Running(data[0], data[1], data[2])
    else:
        return SportsWalking(data[0], data[1], data[2], data[3])


def main(training: Training) -> None:
    """Главная функция."""
    print(training.show_training_info().get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
