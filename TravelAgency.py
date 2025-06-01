import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from abc import ABC, abstractmethod
from datetime import date, timedelta
import random
from typing import List
from PIL import Image, ImageTk


class TravelFactory(ABC):
    @abstractmethod
    def create_ticket(self):
        pass

    @abstractmethod
    def create_hotel(self):
        pass

    @abstractmethod
    def create_tour(self):
        pass

    @abstractmethod
    def get_number_of_flights(self) -> int:
        pass


class BasicTravel(TravelFactory):
    def create_ticket(self):
        return BasicTicket()

    def create_hotel(self):
        return BasicHotel()

    def create_tour(self):
        return BasicTour()

    def get_number_of_flights(self) -> int:
        return random.randint(2, 5)


class PremiumTravel(TravelFactory):
    def create_ticket(self):
        return PremiumTicket()

    def create_hotel(self):
        return PremiumHotel()

    def create_tour(self):
        return PremiumTour()

    def get_number_of_flights(self) -> int:
        return random.randint(1, 3)


class Ticket(ABC):
    def __init__(self):
        self.departure: str = ""
        self.destination: str = ""
        self.date_forward: date = date.today()
        self.date_backward: date = date.today()
        self.price: float = 0.0
        self.time_forward: str = ""
        self.time_backward: str = ""

    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def set_price(self):
        pass

    @abstractmethod
    def set_times(self):
        pass


class BasicTicket(Ticket):
    def get_description(self) -> str:
        return (f"Авиабилет эконом-класс, вылет вперед в {self.time_forward},"
                f" вылет назад в {self.time_backward}, цена: {self.price} руб.")

    def set_price(self):
        self.price = 2 * random.randint(10000, 30000)

    def set_times(self):
        self.time_forward = (f"{random.randint(0, 23)}:"
                             f"{random.randint(0, 5)}{random.randint(0, 9)}")
        self.time_backward = (f"{random.randint(0, 23)}:"
                              f"{random.randint(0, 5)}{random.randint(0, 9)}")


class PremiumTicket(Ticket):
    def get_description(self) -> str:
        return (f"Авиабилет бизнес-класс, вылет вперед в {self.time_forward},"
                f" вылет назад в {self.time_backward}, цена: {self.price} руб.")

    def set_price(self):
        self.price = 2 * random.randint(50000, 100000)

    def set_times(self):
        self.time_forward = (f"{random.randint(0, 23)}:"
                             f"{random.randint(0, 5)}{random.randint(0, 9)}")
        self.time_backward = (f"{random.randint(0, 23)}:"
                              f"{random.randint(0, 5)}{random.randint(0, 9)}")


class Hotel(ABC):
    def __init__(self):
        self.name: str = ""
        self.city: str = ""
        self.check_in: date = date.today()
        self.check_out: date = date.today()
        self.price: float = 0.0
        self.rating: float = 0.0
        self.star: int = 0

    @abstractmethod
    def get_description(self) -> str:
        pass


class BasicHotel(Hotel):
    def get_description(self) -> str:
        nights = (self.check_out - self.check_in).days
        total_price = self.price * nights
        return (f"{self.name}: {self.star}*, рейтинг: {self.rating}, цена за ночь: {self.price} руб., "
                f"{nights} ночей: {total_price} руб.")


class PremiumHotel(Hotel):
    def get_description(self) -> str:
        nights = (self.check_out - self.check_in).days
        total_price = self.price * nights
        return (f"{self.name}: {self.star}*, рейтинг: {self.rating}, цена за ночь: {self.price} руб., "
                f"{nights} ночей: {total_price} руб.")


class Tour(ABC):
    def __init__(self):
        self.name: str = ""
        self.description: str = ""
        self.price: float = 0.0
        self.season: str = ""

    @abstractmethod
    def get_description(self) -> str:
        pass


class BasicTour(Tour):
    def get_description(self) -> str:
        return f"{self.name} - {self.description}, сезон: {self.season}, цена: {self.price} руб."


class PremiumTour(Tour):
    def get_description(self) -> str:
        return f"{self.name} - {self.description}, сезон: {self.season}, цена: {self.price} руб."


class AdditionalServices(ABC):
    @abstractmethod
    def get_description(self) -> str:
        pass

    @abstractmethod
    def get_price(self) -> float:
        pass


class SimCard(AdditionalServices):
    def __init__(self, city: str, selected_tariff: str):
        self.city = city
        self.selected_tariff = selected_tariff
        self.tariffs = {
            "basic": {"data": "10GB", "price": 700},
            "premium": {"data": "50GB", "price": 2000},
        }

    def get_description(self) -> str:
        tariff = self.tariffs[self.selected_tariff]
        return f"SIM-карта ({self.city}): {tariff['data']} интернета (цена: {self.get_price()} руб.)"

    def get_price(self) -> float:
        return self.tariffs[self.selected_tariff]["price"]


class BusPass(AdditionalServices):
    def __init__(self, city: str, duration: int):
        self.city = city
        self.duration = duration
        self.prices = {
            30: 2000,
            7: 800
        }

    def get_description(self) -> str:
        if self.duration > 7:
            return f"Проездной на городской транспорт ({self.city}) на 30 дней (цена: {self.get_price()} руб.)"
        else:
            return f"Проездной на городской транспорт ({self.city}) на 7 дней (цена: {self.get_price()} руб.)"

    def get_price(self) -> float:
        if self.duration > 7:
            return self.prices[30]
        else:
            return self.prices[7]


class GuideBook(AdditionalServices):
    def __init__(self, city: str, language: str = "русский"):
        self.city = city
        self.language = language
        self.price = 800

    def get_description(self) -> str:
        return f"Путеводитель по городу {self.city}, язык {self.language} (цена: {self.get_price()} руб.)"

    def get_price(self) -> float:
        return self.price


class PaymentStrategy(ABC):
    @abstractmethod
    def pay(self, amount: float) -> bool:
        pass


class CreditCard(PaymentStrategy):
    def __init__(self, card_number: str, card_holder: str, expiry_date: str, cvv: str):
        self.card_number = card_number
        self.card_holder = card_holder
        self.expiry_date = expiry_date
        self.cvv = cvv

    def pay(self, amount: float) -> bool:
        if len(self.card_number) != 16 or self.card_holder == "" or self.expiry_date == "" or self.cvv == "":
            return False
        return True


class PayPal(PaymentStrategy):
    def __init__(self, email: str):
        self.email = email

    def pay(self, amount: float) -> bool:
        if self.email.count(".") != 1 or self.email.count("@"):
            return False
        return True


class BankTransfer(PaymentStrategy):
    def __init__(self, account_number: str, bank_name: str):
        self.account_number = account_number
        self.bank_name = bank_name

    def pay(self, amount: float) -> bool:
        if self.account_number == "" or self.bank_name == "":
            return False
        return True


class TravelPackage:
    def __init__(self):
        self.tickets: list[Ticket] = []
        self.hotels: list[Hotel] = []
        self.tours: list[Tour] = []
        self.services: list[AdditionalServices] = []

    def add_ticket(self, ticket: Ticket):
        self.tickets.append(ticket)

    def add_hotel(self, hotel: Hotel):
        self.hotels.append(hotel)

    def add_tour(self, tour: Tour):
        self.tours.append(tour)

    def add_service(self, service: AdditionalServices):
        self.services.append(service)

    def get_total_price(self) -> float:
        total_price = 0
        for ticket in self.tickets:
            total_price += ticket.price
        for hotel in self.hotels:
            nights = (hotel.check_out - hotel.check_in).days
            total_price += hotel.price * nights
        for tour in self.tours:
            total_price += tour.price
        for service in self.services:
            total_price += service.get_price()
        return total_price

    def get_description(self) -> str:
        desc = "Ваше путешествие:\n\n"
        desc += "Билеты:\n"
        for ticket in self.tickets:
            desc += f"- {ticket.get_description()}\n"

        desc += "\nОтель:\n"
        for hotel in self.hotels:
            desc += f"- {hotel.get_description()}\n"

        if self.tours:
            desc += "\nТуры:\n"
            for tour in self.tours:
                desc += f"- {tour.get_description()}\n"

        if self.services:
            desc += "\nПолезные услуги:\n"
            for service in self.services:
                desc += f"- {service.get_description()}\n"

        desc += f"\nОбщая стоимость: {self.get_total_price()} руб."
        return desc


class TravelPackageBuilder:
    def __init__(self, factory: TravelFactory):
        self.factory = factory
        self.reset()

    def reset(self):
        self.travel_package = TravelPackage()

    def add_ticket(self, departure: str, destination: str, date_forward: date, date_backward: date,
                   price: float, time_forward: str, time_backward: str):
        ticket = self.factory.create_ticket()
        ticket.departure = departure
        ticket.destination = destination
        ticket.date_forward = date_forward
        ticket.date_backward = date_backward
        ticket.price = price
        ticket.time_forward = time_forward
        ticket.time_backward = time_backward
        self.travel_package.add_ticket(ticket)

    def add_hotel(self, name: str, city: str, check_in: date, check_out: date, price_per_night: float,
                  rating: float, star: int):
        hotel = self.factory.create_hotel()
        hotel.name = name
        hotel.city = city
        hotel.check_in = check_in
        hotel.check_out = check_out
        hotel.price = price_per_night
        hotel.rating = rating
        hotel.star = star
        self.travel_package.add_hotel(hotel)

    def add_tour(self, name: str, description: str, price: float, season: str):
        tour = self.factory.create_tour()
        tour.name = name
        tour.description = description
        tour.price = price
        tour.season = season
        self.travel_package.add_tour(tour)

    def add_service(self, service: AdditionalServices):
        self.travel_package.add_service(service)

    def get_package(self) -> TravelPackage:
        package = self.travel_package
        self.reset()
        return package


class TravelService:
    def __init__(self):
        self.factories = {
            "basic": BasicTravel(),
            "premium": PremiumTravel()
        }

        self.cities = ["Нижний Новгород", "Санкт-Петербург", "Москва", "Анапа", "Кострома", "Владимир",
                       "Великий Устюг", "Вологда", "Архангельск"]

        self.hotels_data = {
            "Архангельск": [
                {"name": "Пур-Наволок", "type": "basic", "price": 3500, "rating": 3.8, "star": 3},
                {"name": "Двина", "type": "premium", "price": 8000, "rating": 4.5, "star": 4}
            ],
            "Вологда": [
                {"name": "Спасская", "type": "basic", "price": 3000, "rating": 4.0, "star": 3},
                {"name": "Атриум", "type": "premium", "price": 7500, "rating": 4.7, "star": 4}
            ],
            "Великий Устюг": [
                {"name": "Сухона", "type": "basic", "price": 2800, "rating": 3.9, "star": 2},
                {"name": "Вотчина Деда Мороза", "type": "premium", "price": 10000, "rating": 4.8, "star": 4}
            ],
            "Владимир": [
                {"name": "Заря", "type": "basic", "price": 3200, "rating": 3.7, "star": 3},
                {"name": "Русская деревня", "type": "premium", "price": 8500, "rating": 4.6, "star": 4}
            ],
            "Кострома": [
                {"name": "Волга", "type": "basic", "price": 3500, "rating": 4.1, "star": 3},
                {"name": "Аристократ", "type": "premium", "price": 9000, "rating": 4.7, "star": 4}
            ],
            "Анапа": [
                {"name": "Алые паруса", "type": "basic", "price": 4000, "rating": 4.2, "star": 3},
                {"name": "Малая бухта", "type": "premium", "price": 15000, "rating": 4.9, "star": 5}
            ],
            "Москва": [
                {"name": "Ибис", "type": "basic", "price": 5000, "rating": 4.0, "star": 3},
                {"name": "Ritz-Carlton", "type": "premium", "price": 25000, "rating": 4.9, "star": 5},
                {"name": "Метрополь", "type": "premium", "price": 30000, "rating": 4.8, "star": 5}
            ],
            "Санкт-Петербург": [
                {"name": "Станция L1", "type": "basic", "price": 4500, "rating": 4.1, "star": 3},
                {"name": "Коринтия", "type": "premium", "price": 20000, "rating": 4.9, "star": 5},
                {"name": "Астория", "type": "premium", "price": 28000, "rating": 4.8, "star": 5}
            ],
            "Нижний Новгород": [
                {"name": "Азимут", "type": "basic", "price": 3800, "rating": 3.9, "star": 3},
                {"name": "Sheraton", "type": "premium", "price": 12000, "rating": 4.7, "star": 5}
            ]
        }

        self.tours_data = {
            "Архангельск": [
                {"name": "Музей деревянного зодчества", "description": "Экскурсия в музей Малые Корелы", "price": 1500,
                 "season": "все", "type": "basic"},
                {"name": "Северодвинск", "description": "Тур в город корабелов", "price": 3500,
                 "season": "лето", "type": "premium"}
            ],
            "Вологда": [
                {"name": "Вологодский кремль", "description": "Обзорная экскурсия по кремлю", "price": 1200,
                 "season": "все", "type": "basic"},
                {"name": "Музей кружева", "description": "Экскурсия в музей вологодского кружева", "price": 1800,
                 "season": "все", "type": "premium"}
            ],
            "Великий Устюг": [
                {"name": "Резиденция Деда Мороза", "description": "Посещение вотчины Деда Мороза", "price": 2500,
                 "season": "зима", "type": "basic"},
                {"name": "Обзорная экскурсия", "description": "Тур по историческому центру", "price": 2000,
                 "season": "все", "type": "basic"}
            ],
            "Владимир": [
                {"name": "Золотые ворота", "description": "Экскурсия к памятнику ЮНЕСКО", "price": 1500,
                 "season": "все", "type": "basic"},
                {"name": "Боголюбово", "description": "Поездка в церковь Покрова на Нерли", "price": 3000,
                 "season": "лето", "type": "premium"}
            ],
            "Кострома": [
                {"name": "Ипатьевский монастырь", "description": "Экскурсия в исторический монастырь", "price": 1800,
                 "season": "все", "type": "basic"},
                {"name": "Музей сыра", "description": "Дегустация костромских сыров", "price": 2500,
                 "season": "все", "type": "premium"}
            ],
            "Анапа": [
                {"name": "Археологический музей", "description": "Экскурсия по античным находкам", "price": 1200,
                 "season": "все", "type": "basic"},
                {"name": "Морская прогулка", "description": "Прогулка на катере вдоль побережья", "price": 3500,
                 "season": "лето", "type": "premium"}
            ],
            "Москва": [
                {"name": "Красная площадь", "description": "Обзорная экскурсия", "price": 2000,
                 "season": "все", "type": "basic"},
                {"name": "Третьяковская галерея", "description": "Экскурсия с искусствоведом", "price": 5000,
                 "season": "все", "type": "premium"},
                {"name": "Москва-Сити", "description": "Тур по небоскребам с подъемом", "price": 6000,
                 "season": "все", "type": "premium"}
            ],
            "Санкт-Петербург": [
                {"name": "Эрмитаж", "description": "Экскурсия по главному музею", "price": 3000,
                 "season": "все", "type": "basic"},
                {"name": "Петергоф", "description": "Тур в летнюю резиденцию", "price": 4500,
                 "season": "лето", "type": "premium"},
                {"name": "Белые ночи", "description": "Ночная экскурсия по разводным мостам", "price": 5000,
                 "season": "лето", "type": "premium"}
            ],
            "Нижний Новгород": [
                {"name": "Нижегородский кремль", "description": "Обзорная экскурсия", "price": 1800,
                 "season": "все", "type": "basic"},
                {"name": "Горьковские места", "description": "Литературный тур", "price": 2500,
                 "season": "все", "type": "premium"}
            ]
        }

        self.SimCardTariffs = ["basic", "premium"]
        self.languages = ["русский", "английский"]

    def get_season(self, travel_date: date) -> str:
        month = travel_date.month
        if month in [12, 1, 2]:
            return "зима"
        elif month in [3, 4, 5]:
            return "весна"
        elif month in [6, 7, 8]:
            return "лето"
        else:
            return "осень"

    def generate_tickets(self, departure: str, destination: str, date_forward: date, date_backward: date,
                         package_type: str) -> List[Ticket]:
        tickets = []
        factory = self.factories[package_type]

        for i in range(factory.get_number_of_flights()):
            ticket = factory.create_ticket()
            ticket.departure = departure
            ticket.destination = destination
            ticket.date_forward = date_forward
            ticket.date_backward = date_backward
            ticket.set_times()
            ticket.set_price()

            tickets.append(ticket)

        return tickets

    def get_available_hotels(self, city: str, package_type: str, start_date: date, end_date: date) -> List[Hotel]:
        hotels = []
        city_hotels = self.hotels_data.get(city)
        factory = self.factories[package_type]

        for hotel_data in city_hotels:
            if package_type == hotel_data["type"]:
                hotel = factory.create_hotel()

                hotel.name = hotel_data["name"]
                hotel.city = city
                hotel.price = hotel_data["price"]
                hotel.rating = hotel_data["rating"]
                hotel.star = hotel_data["star"]
                hotel.check_in = start_date
                hotel.check_out = end_date

                hotels.append(hotel)

        return hotels

    def get_available_tours(self, city: str, package_type: str, travel_date: date) -> List[Tour]:
        tours = []
        season = self.get_season(travel_date)
        city_tours = self.tours_data.get(city)
        factory = self.factories[package_type]

        for tour_data in city_tours:
            if (package_type == tour_data["type"]) or (package_type == "premium"):
                if tour_data["season"] == "все" or tour_data["season"] == season:
                    tour = factory.create_tour()
                    tour.name = tour_data["name"]
                    tour.description = tour_data["description"]
                    tour.price = tour_data["price"]
                    tour.season = tour_data["season"]

                    tours.append(tour)

        return tours

    def get_available_services(self, city: str, duration: int, package_type: str) -> List[AdditionalServices]:
        services = []

        sim_card = SimCard(city, package_type)
        services.append(sim_card)

        transport_pass = BusPass(city, duration)
        services.append(transport_pass)

        for lang in self.languages:
            guide_book = GuideBook(city, lang)
            services.append(guide_book)

        return services

    def create_package_builder(self, package_type: str) -> TravelPackageBuilder:
        factory = self.factories.get(package_type)
        return TravelPackageBuilder(factory)


class TravelApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Сервис путешествий")
        self.root.geometry("1200x700+0+10")

        self.travel_service = TravelService()

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.setup_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.setup_tab, text="Выбор параметров")

        self.results_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.results_tab, text="Результаты")

        self.payment_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.payment_tab, text="Оплата")

        self.city_images = {}
        self.load_city_images()

        self.setup_parameters_tab()
        self.setup_results_tab()
        self.setup_payment_tab()

        self.available_tickets = []
        self.available_hotels = []
        self.available_tours = []
        self.available_services = []
        self.selected_ticket = None
        self.selected_hotel = None
        self.selected_tours = []
        self.selected_services = []
        self.current_city_image = None
        self.travel_package = None

    def load_city_images(self):
        cities = self.travel_service.cities

        for city in cities:
            try:
                image_path = f"{city}.jpg"
                image = Image.open(image_path)
                if city == "Москва" or city == "Нижний Новгород":
                    image = image.resize((470, 600))
                else:
                    image = image.resize((600, 400))
            except FileNotFoundError:
                print(f"Изображение для города {city} не найдено")
                image = Image.new('RGB', (400, 300), color='black')
            photo = ImageTk.PhotoImage(image)
            self.city_images[city] = photo

    def setup_parameters_tab(self):
        parameters_frame = ttk.Frame(self.setup_tab)
        parameters_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.image_frame = ttk.Label(self.setup_tab)
        self.image_frame.pack(fill=tk.BOTH, padx=5, pady=50, anchor=tk.NE)

        ttk.Label(parameters_frame, text="Город отправления:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.departure_entry = ttk.Entry(parameters_frame)
        self.departure_entry.grid(row=0, column=0, padx=200, pady=5, sticky=tk.EW)
        self.departure_entry.insert(0, "Ярославль")

        ttk.Label(parameters_frame, text="Город назначения:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.destination_combo = ttk.Combobox(parameters_frame, values=self.travel_service.cities, state='readonly')
        self.destination_combo.grid(row=1, column=0, padx=200, pady=5, sticky=tk.EW)
        self.destination_combo.current(0)
        self.destination_combo.bind("<<ComboboxSelected>>", self.update_image)

        self.update_image(self)

        ttk.Label(parameters_frame, text="Дата начала (ГГГГ-ММ-ДД):").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.start_date_entry = ttk.Entry(parameters_frame)
        self.start_date_entry.grid(row=2, column=0, padx=200, pady=5, sticky=tk.EW)
        self.start_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        ttk.Label(parameters_frame, text="Дата окончания (ГГГГ-ММ-ДД):").grid(row=3, column=0, padx=5, pady=5,
                                                                              sticky=tk.W)
        self.end_date_entry = ttk.Entry(parameters_frame)
        self.end_date_entry.grid(row=3, column=0, padx=200, pady=5, sticky=tk.EW)
        self.end_date_entry.insert(0, (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"))

        ttk.Label(parameters_frame, text="Тип путешествия:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.travel_type_var = tk.StringVar(value="basic")
        (ttk.Radiobutton(parameters_frame, text="Базовый", variable=self.travel_type_var, value="basic").grid
         (row=4, column=0, padx=200, pady=5, sticky=tk.W))
        (ttk.Radiobutton(parameters_frame, text="Премиум", variable=self.travel_type_var, value="premium").grid
         (row=5, column=0, padx=200, pady=5, sticky=tk.W))

        self.search_options_button = ttk.Button(parameters_frame, text="Поиск вариантов", command=self.search_options)
        self.search_options_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.tickets_frame = ttk.LabelFrame(parameters_frame, text="Билеты")
        self.tickets_frame.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.hotels_frame = ttk.LabelFrame(parameters_frame, text="Отели")
        self.hotels_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.tours_frame = ttk.LabelFrame(parameters_frame, text="Экскурсии")
        self.tours_frame.grid(row=9, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.services_frame = ttk.LabelFrame(parameters_frame, text="Полезные услуги")
        self.services_frame.grid(row=10, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.create_package_button = ttk.Button(parameters_frame, text="Создать пакет", command=self.create_package,
                                                state=tk.DISABLED)
        self.create_package_button.grid(row=11, column=0, columnspan=2, pady=10)

    def update_image(self, event):
        city = self.destination_combo.get()
        self.current_city_image = self.city_images[city]
        self.image_frame.config(image=self.current_city_image)

    def search_options(self):
        try:
            departure = self.departure_entry.get().strip()
            destination = self.destination_combo.get()
            start_date = date.fromisoformat(self.start_date_entry.get().strip())
            end_date = date.fromisoformat(self.end_date_entry.get().strip())
            package_type = self.travel_type_var.get()
            duration = (end_date - start_date).days

            if not departure:
                raise ValueError("Введите город отправления")
            if end_date <= start_date:
                raise ValueError("Дата окончания должна быть позже даты начала")
            if start_date < date.today():
                raise ValueError("Ваш рейс улетел")

            self.available_tickets = self.travel_service.generate_tickets(departure, destination, start_date, end_date,
                                                                          package_type)
            self.show_tickets()

            self.available_hotels = self.travel_service.get_available_hotels(destination, package_type, start_date,
                                                                             end_date)
            self.show_hotels()

            self.available_tours = self.travel_service.get_available_tours(destination, package_type, start_date)
            self.show_tours()

            self.available_services = self.travel_service.get_available_services(destination, duration, package_type)
            self.show_services()

            self.create_package_button.config(state=tk.NORMAL)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def show_tickets(self):
        for widget in self.tickets_frame.winfo_children():
            widget.destroy()

        self.ticket_var = tk.IntVar(value=-1)
        for i, ticket in enumerate(self.available_tickets):
            rb = ttk.Radiobutton(
                self.tickets_frame,
                text=ticket.get_description(),
                variable=self.ticket_var,
                value=i
            )
            rb.grid(sticky=tk.W)

    def show_hotels(self):
        for widget in self.hotels_frame.winfo_children():
            widget.destroy()

        self.hotel_var = tk.IntVar(value=-1)
        for i, hotel in enumerate(self.available_hotels):
            rb = ttk.Radiobutton(
                self.hotels_frame,
                text=hotel.get_description(),
                variable=self.hotel_var,
                value=i
            )
            rb.grid(sticky=tk.W)

    def show_tours(self):
        for widget in self.tours_frame.winfo_children():
            widget.destroy()

        self.tour_vars = []
        for i, tour in enumerate(self.available_tours):
            var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(
                self.tours_frame,
                text=tour.get_description(),
                variable=var
            )
            cb.grid(sticky=tk.W)
            self.tour_vars.append((i, var))

    def show_services(self):
        for widget in self.services_frame.winfo_children():
            widget.destroy()

        self.service_vars = []
        for i, service in enumerate(self.available_services):
            var = tk.IntVar(value=0)
            cb = ttk.Checkbutton(
                self.services_frame,
                text=f"{service.get_description()} (цена: {service.get_price()} руб.)",
                variable=var
            )
            cb.grid(sticky=tk.W)
            self.service_vars.append((i, var))

    def create_package(self):
        try:
            ticket_idx = self.ticket_var.get()
            hotel_idx = self.hotel_var.get()

            if ticket_idx == -1:
                raise ValueError("Выберите билет")
            if hotel_idx == -1:
                raise ValueError("Выберите отель")

            self.selected_ticket = self.available_tickets[ticket_idx]
            self.selected_hotel = self.available_hotels[hotel_idx]
            self.selected_tours = []
            self.selected_services = []

            for i, var in self.tour_vars:
                if var.get() == 1:
                    self.selected_tours.append(self.available_tours[i])

            for i, var in self.service_vars:
                if var.get() == 1:
                    self.selected_services.append(self.available_services[i])

            builder = self.travel_service.create_package_builder(self.travel_type_var.get())

            builder.add_ticket(
                departure=self.selected_ticket.departure,
                destination=self.selected_ticket.destination,
                date_forward=self.selected_ticket.date_forward,
                date_backward=self.selected_ticket.date_backward,
                price=self.selected_ticket.price,
                time_forward=self.selected_ticket.time_forward,
                time_backward=self.selected_ticket.date_backward
            )

            builder.add_hotel(
                name=self.selected_hotel.name,
                city=self.selected_hotel.city,
                check_in=self.selected_hotel.check_in,
                check_out=self.selected_hotel.check_out,
                price_per_night=self.selected_hotel.price,
                rating=self.selected_hotel.rating,
                star=self.selected_hotel.star
            )

            for tour in self.selected_tours:
                builder.add_tour(
                    name=tour.name,
                    description=tour.description,
                    price=tour.price,
                    season=tour.season
                )

            for service in self.selected_services:
                builder.add_service(service)

            self.travel_package = builder.get_package()

            self.show_results(self.travel_package)

            self.notebook.select(self.results_tab)

        except ValueError as e:
            messagebox.showerror("Ошибка", str(e))

    def setup_results_tab(self):
        self.results_text = tk.Text(self.results_tab, wrap=tk.WORD, font='Times 14')
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.results_text.insert(tk.END, "Здесь будет отображаться ваше путешествие после создания.")
        self.results_text.config(state=tk.DISABLED)

    def show_results(self, package):
        self.results_text.config(state=tk.NORMAL)
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, package.get_description())
        self.results_text.config(state=tk.DISABLED)

        pay_button = ttk.Button(self.results_tab, text="Перейти к оплате",
                                command=lambda: self.notebook.select(self.payment_tab))
        pay_button.pack(pady=10)

    def setup_payment_tab(self):
        self.payment_frame = ttk.Frame(self.payment_tab)
        self.payment_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        ttk.Label(self.payment_frame, text="Способ оплаты:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.payment_method = ttk.Combobox(self.payment_frame,
                                           values=["Кредитная карта", "PayPal", "Банковский перевод"], state='readonly')
        self.payment_method.grid(row=0, column=1, padx=5, pady=5, sticky=tk.EW)
        self.payment_method.current(0)
        self.payment_method.bind("<<ComboboxSelected>>", self.update_payment_fields)

        self.payment_fields_frame = ttk.Frame(self.payment_frame)
        self.payment_fields_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky=tk.EW)

        self.pay_button = ttk.Button(self.payment_frame, text="Оплатить", command=self.process_payment)
        self.pay_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.setup_credit_card_fields()

    def update_payment_fields(self, event):
        for widget in self.payment_fields_frame.winfo_children():
            widget.destroy()

        method = self.payment_method.get()
        if method == "Кредитная карта":
            self.setup_credit_card_fields()
        elif method == "PayPal":
            self.setup_paypal_fields()
        elif method == "Банковский перевод":
            self.setup_bank_transfer_fields()

    def setup_credit_card_fields(self):
        ttk.Label(self.payment_fields_frame, text="Номер карты:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.card_number = ttk.Entry(self.payment_fields_frame)
        self.card_number.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(self.payment_fields_frame, text="Держатель карты:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.card_holder = ttk.Entry(self.payment_fields_frame)
        self.card_holder.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(self.payment_fields_frame, text="Срок действия:").grid(row=2, column=0, padx=5, pady=2, sticky=tk.W)
        self.card_expiry = ttk.Entry(self.payment_fields_frame)
        self.card_expiry.grid(row=2, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(self.payment_fields_frame, text="CVV:").grid(row=3, column=0, padx=5, pady=2, sticky=tk.W)
        self.card_cvv = ttk.Entry(self.payment_fields_frame, show="*")
        self.card_cvv.grid(row=3, column=1, padx=5, pady=2, sticky=tk.EW)

    def setup_paypal_fields(self):
        ttk.Label(self.payment_fields_frame, text="Email PayPal:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.paypal_email = ttk.Entry(self.payment_fields_frame)
        self.paypal_email.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

    def setup_bank_transfer_fields(self):
        ttk.Label(self.payment_fields_frame, text="Номер счета:").grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)
        self.account_number = ttk.Entry(self.payment_fields_frame)
        self.account_number.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)

        ttk.Label(self.payment_fields_frame, text="Банк:").grid(row=1, column=0, padx=5, pady=2, sticky=tk.W)
        self.bank_name = ttk.Entry(self.payment_fields_frame)
        self.bank_name.grid(row=1, column=1, padx=5, pady=2, sticky=tk.EW)

    def process_payment(self):
        try:
            method = self.payment_method.get()
            amount = self.travel_package.get_total_price()

            if method == "Кредитная карта":
                strategy = CreditCard(
                    card_number=self.card_number.get(),
                    card_holder=self.card_holder.get(),
                    expiry_date=self.card_expiry.get(),
                    cvv=self.card_cvv.get()
                )
            elif method == "PayPal":
                strategy = PayPal(email=self.paypal_email.get())
            else:
                strategy = BankTransfer(
                    account_number=self.account_number.get(),
                    bank_name=self.bank_name.get()
                )

            if strategy.pay(amount):
                messagebox.showinfo("Успех", "Оплата прошла успешно! \n Вперед идет локомотив!")
            else:
                messagebox.showerror("Ошибка", "Не удалось выполнить оплату "
                                               "\n(проверьте корректность ввода данных)")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при обработке платежа")


root = tk.Tk()
app = TravelApp(root)
root.mainloop()
