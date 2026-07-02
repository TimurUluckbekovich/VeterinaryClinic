from abc import ABC, abstractmethod
import random

class VaccinationMixin:
    def __init__(self):
        self.is_vaccinated = False

    def vaccinate(self):
        self.is_vaccinated = True

    def get_vaccination_status(self):
        return "Вакцинирован" if self.is_vaccinated else "Не вакцинирован"

class MedicalHiistoryMixin:
    def __init__(self):
        self._history = []

    def add_diagnosis(self, diagnosis: str):
        self._history.append(diagnosis)

    def get_history(self):
        return self._history if self._history else ["История болезней чиста."]

class Animal(ABC):
    def __init__(self, animal_id,name, species, age):
        self.__id = animal_id
        self.name = name
        self.species = species
        self.age = age

    def get_id(self):
        return self.__id

    @abstractmethod
    def make_sound(self):
        pass

    @abstractmethod
    def show_info(self):
        pass

class Pet(Animal, VaccinationMixin, MedicalHiistoryMixin):
    def __init__(self, animal_id, name, species, age, owner_id=None):
        Animal.__init__(self, animal_id, name, species, age)
        VaccinationMixin.__init__(self)
        MedicalHiistoryMixin.__init__(self)
        self.owner_id = owner_id

    def show_info(self):
        return f"Питомец {self.name}, Вид {self.species}, Возраст {self.age} лет"

    def make_sound(self):
        return "Издаёт неопределённый звук"

    def __str__(self):
        return f"Питомец {self.name} ({self.species})"

    def __repr__(self):
        return f"Pet(id={self.get_id()}, name='{self.species}', species='{self.species}')"

    def __len__(self):
        return len(self._history)

    def __eq__(self, other):
        if not isinstance(other, Pet):
            return False
        return self.get_id() == other.get_id()

    @staticmethod
    def is_adult(age):
        return age >= 1

    @staticmethod
    def generate_card_number():
        return f"MED-{random.randint(1000,9999)}"

    @classmethod
    def from_db(cls, row):
        if not row:
            return None
        return cls(animal_id=row[0], name=row[1], species=row[2], age=row[3], owner_id=row[4])

    @classmethod
    def from_dict(cls, data):
        if not data:
            return None
        return cls(
            animal_id=data.get("id"),
            name=data.get("name"),
            species=data.get("species"),
            age=data.get("age"),
            owner_id=data.get("owner_id")
        )


class Dog(Pet):
    def make_sound(self):
        return "Гав-Гав!"


class Cat(Pet):
    def make_sound(self):
        return "Мяу!"


class Person:
    def __init__(self, person_id, full_name, phone=None):
        self.__id = person_id
        self.full_name = full_name
        self._phone = phone

    def get_phone(self):
        return self._phone

    def set_phone(self, new_phone):
        self._phone = new_phone

    def get_id(self):
        return self.__id

    def show_profile(self):
        return f"Пользователь: {self.full_name}"

class Owner(Person):
    def __init__(self, owner_id, full_name, phone):
        super().__init__(owner_id, full_name, phone)

    def show_profile(self):
        return f"[Клиент клиники] {self.full_name}, Контакты: {self._phone}"

    @classmethod
    def from_db(cls, row):
        if not row:
            return None
        return cls(owner_id=row[0], full_name=row[1], phone=row[2])


class Doctor(Person):
    def __init__(self, doctor_id, full_name, specialization, phone="Не указан"):
        super().__init__(doctor_id, full_name, phone)
        self.specialization = specialization

    def show_profile(self):
        return f"[Ветеринар] {self.full_name}, Специализация: {self.specialization}"

    @classmethod
    def from_db(cls, row):
        if not row:
            return None
        return cls(doctor_id=row[0], full_name=row[1], specialization=row[2])


class Administrator(Person):
    def __init__(self, admin_id, full_name, phone, shift_time):
        super().__init__(admin_id, full_name, phone)
        self.shift_time = shift_time

    def show_profile(self):
        return f"[Администратор] {self.full_name}, График смены: {self.shift_time}"






