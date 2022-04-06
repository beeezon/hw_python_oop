from typing import Dict, List, Type


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
        self.duration_hour = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration_hour:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    HOURS_TO_MINUTES: int = 60

    def __init__(self,
                 action: int,  # кол-во действий
                 duration: float,  # длительность
                 weight: float,  # вес
                 ) -> None:
        self.action = action
        self.duration_hour = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_hour

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass  # оставляем пустым, изменяем в классе - наследнике.

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration_hour,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    AVERAGE_SPEED_MULTIPLIER: int = 18
    AVERAGE_SPEED_SUBTRACT: int = 20

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.AVERAGE_SPEED_MULTIPLIER * self.get_mean_speed()
                - self.AVERAGE_SPEED_SUBTRACT)
                * self.weight_kg / self.M_IN_KM
                * (self.duration_hour * self.HOURS_TO_MINUTES))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    MASS_MULTIPLIER_ONE: float = 0.035
    DEGREE_OF_AVERAGE_SPEED: float = 2
    MASS_MULTIPLIER_TWO: float = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_meter = height

    def get_spent_calories(self) -> float:
        return ((self.MASS_MULTIPLIER_ONE * self.weight_kg
                + (self.get_mean_speed()**self.DEGREE_OF_AVERAGE_SPEED
                 // self.height_meter) * self.MASS_MULTIPLIER_TWO
                 * self.weight_kg)
                * (self.duration_hour * self.HOURS_TO_MINUTES))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    ADDITIONAL_COEFFICIENT_TO_SPEED: int = 1.1
    CALORIES_MULTIPLIER: int = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_meter = length_pool  # длинна бассейна
        self.count_pool = count_pool  # сколько раз проплыл

    def get_mean_speed(self) -> float:
        """Расчет средней скорости."""
        return (self.length_pool_meter * self.count_pool
                / self.M_IN_KM / self.duration_hour)

    def get_spent_calories(self) -> float:
        """Расчет калорий."""
        return ((self.get_mean_speed() + self.ADDITIONAL_COEFFICIENT_TO_SPEED)
                * self.CALORIES_MULTIPLIER * self.weight_kg)


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    type_workout: Dict[str, Type[Training]] = {'SWM': Swimming,
                                               'RUN': Running,
                                               'WLK': SportsWalking}
    return (type_workout.get(workout_type)(*data))


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
