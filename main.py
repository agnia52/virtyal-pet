import json

import pygame as pg
import random

pg.init()


SCREEN_WIDHT = 900
SCREEN_HEIGHT = 550

ICON_SIZE = 80 

DOG_WIDHT = 310
DOG_HEIGHT = 500

BUTTON_WIDHT = 200
BUTTON_HEIGHT = 60

FOOD_SIZE = 200
TOY_SIZE = 100

GRID = 10 

FPS = 60

font = pg.font.Font(None, 40)
font_mini = pg.font.Font(None, 15)
font_maxi = pg.font.Font(None, 200)

def load_image(file, widht, height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image, (widht, height))
    return image

def text_render(text):
    return font.render(str(text), True, "black")

new_game_data = {"happiness": 100, "satiety":100 , "health": 100, "money": 0, "coins_ptr_second": 1, "costs_of_upgrade": {"100": False, "1000": False, "5000": False, "10000": False}, "clothes": [{"name": "Синяя футболка", "price": 10, "image": "images/items/blue t-shirt.png", "is_using": False, "is_bought": False}, {"name": "Ботинки", "price": 50, "image": "images/items/boots.png", "is_using": False, "is_bought": False}, {"name": "Шляпа", "price": 50, "image": "images/items/hat.png", "is_using": False, "is_bought": False}]}

class Toy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        file = random.choice(["images/toys/ball.png", "images/toys/blue bone.png", "images/toys/red bone.png"])

        self.image = load_image(file, TOY_SIZE, TOY_SIZE)
        self.rect = self.image.get_rect()

        self.rect.x = random.randint(GRID*9,SCREEN_WIDHT - GRID*23)
        self.rect.y = 30

    def update(self):
        self.rect.y += 2 

class Dog(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)

        self.image = load_image("images/dog.png", DOG_WIDHT // 2, DOG_HEIGHT // 2)
        self.rect = self.image.get_rect()

        self.rect.centerx = SCREEN_WIDHT // 2
        self.rect.centery = SCREEN_HEIGHT - GRID * 14

    def update(self):
        # keys - клавиши на клавиатуре 
        keys = pg.key.get_pressed()
        # если нажата клавиша K_a
        if keys[pg.K_a]:
            # вычитаем из х 2
            self.rect.x -= 2
        # если нажата клавиша K_d
        if keys[pg.K_d]:
            # прибавляем к х 2
            self.rect.x += 2

class MiniGame:
    def __init__(self, game):
        self.game = game
        self.background = load_image("images/game_background.png", SCREEN_WIDHT, SCREEN_HEIGHT)

        self.new_game()

    def new_game(self):
        self.toys = pg.sprite.Group()
        self.dog = Dog()
        self.score = 0

        self.start_time = pg.time.get_ticks()
        self.interval = 1000 * 15

    def update(self):
        self.toys.update()
        self.dog.update()

        if random.randint(0,30) == 0: 
            self.toys.add(Toy())

        hits = pg.sprite.spritecollide(self.dog, self.toys, True, pg.sprite.collide_rect_ratio(0.6))
        self.score += len(hits)

        if pg.time.get_ticks() - self.start_time > self.interval:
            self.game.happiness += int(self.score)
            self.game.mode = "Main"

    def draw(self, screen):
        screen.blit(self.background, (0,0))
        screen.blit(self.dog.image, self.dog.rect)
        self.toys.draw(screen)
        score_text = text_render(self.score)
        screen.blit(score_text,(GRID * 12, GRID * 9))

class Food:
    def __init__(self, name, price, file, satiety, medicine_pover=0):
        self.name = name
        self.price = price
        self.satiety = satiety
        self.medicine_pover = medicine_pover
        self.image = load_image(file, FOOD_SIZE, FOOD_SIZE)

class FoodMenu:
    def __init__(self,game):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDHT, SCREEN_HEIGHT)

        self.items = [Food("Мясо", 30, "images/food/meat.png", 10),
                      Food("Корм", 30, "images/food/dog food.png", 1),
                      Food("Элитный корм", 30, "images/food/dog food elite.png", 25, medicine_pover=2),
                      Food("Лекарство", 30, "images/food/medicine.png", 0, medicine_pover=10),]

        self.current_item = 0

        self.render_item()
 

        self.next_button = Button("Вперёд", SCREEN_WIDHT - BUTTON_WIDHT - GRID * 10, SCREEN_HEIGHT - GRID * 14, 
                                    widht=BUTTON_WIDHT // 1.2, height=BUTTON_HEIGHT // 1.2, func=self.to_next)

        self.previous_button = Button("Назад", GRID * 14, SCREEN_HEIGHT - GRID * 14, 
                                    widht=BUTTON_WIDHT // 1.2, height=BUTTON_HEIGHT // 1.2, func=self.to_previous)

        self.buy_button = Button("Съесть", SCREEN_WIDHT // 2 - int(BUTTON_WIDHT // 1.5) // 2, SCREEN_HEIGHT // 2 + GRID * 10, 
                                    widht=BUTTON_WIDHT // 1.5, height=int(BUTTON_HEIGHT // 1.5),
                                    func=self.buy_and_eat)

    def render_item(self):
        self.item_rect = self.items[0].image.get_rect()
        self.item_rect.center = (SCREEN_WIDHT // 2, SCREEN_HEIGHT // 2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDHT // 2, GRID * 18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDHT // 2, GRID * 12)

    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
            self.render_item()

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
            self.render_item()

    def buy_and_eat(self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.game.satiety += self.items[self.current_item].satiety
            self.game.health += self.items[self.current_item].medicine_pover

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)
        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)

        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.buy_button.draw(screen)

class Item:
    def __init__(self, name, price, file, is_using, is_bought):
        self.name = name
        self.price = price
        self.file = file
        self.image = load_image(file, DOG_WIDHT // 1.7, DOG_HEIGHT // 1.7)
        self.is_using = is_using
        self.is_bought = is_bought
        self.full_image = load_image(file, DOG_WIDHT, DOG_HEIGHT)

class Clothesmenu:
    def __init__(self, game, data):
        self.game = game
        self.menu_page = load_image("images/menu/menu_page.png", SCREEN_WIDHT, SCREEN_HEIGHT)
        self.items = []
        for item in data:
            item_object = Item(item["name"], item["price"], item["image"], item["is_using"], item["is_bought"])
            self.items.append(item_object)
        self.current_item = 0
        self.render_item()

        self.next_button = Button("Вперёд", SCREEN_WIDHT - BUTTON_WIDHT - GRID * 10, SCREEN_HEIGHT - GRID * 14, 
                                    widht=BUTTON_WIDHT // 1.2, height=BUTTON_HEIGHT // 1.2, func=self.to_next)

        self.previous_button = Button("Назад", GRID * 14, SCREEN_HEIGHT - GRID * 14, 
                                    widht=BUTTON_WIDHT // 1.2, height=BUTTON_HEIGHT // 1.2, func=self.to_previous)

        self.use_button = Button("Надеть", GRID * 14, SCREEN_HEIGHT - BUTTON_HEIGHT - GRID * 14, 
                                    widht=BUTTON_WIDHT // 1.2, height=int(BUTTON_HEIGHT // 1.2),
                                    func=self.use_item)

        self.buy_button = Button("Купить", SCREEN_WIDHT // 2 - int(BUTTON_WIDHT // 1.5) // 2, SCREEN_HEIGHT // 2 + GRID * 10, 
                                    widht=BUTTON_WIDHT // 1.5, height=int(BUTTON_HEIGHT // 1.5),
                                    func=self.buy)

        self.use_text = text_render("Надето")   
        self.use_text_rect = self.use_text.get_rect()   
        self.use_text_rect.midright = (SCREEN_WIDHT - GRID * 15, GRID * 13)       

        self.buy_text = text_render("Куплено")   
        self.buy_text_rect = self.buy_text.get_rect()   
        self.buy_text_rect.midright = (SCREEN_WIDHT - GRID * 14, GRID * 20)
                    
        self.buttom_label_off = load_image("images/menu/bottom_label_off.png", SCREEN_WIDHT, SCREEN_HEIGHT)
        self.buttom_label_on = load_image("images/menu/bottom_label_on.png", SCREEN_WIDHT, SCREEN_HEIGHT)
        self.top_label_off = load_image("images/menu/top_label_off.png", SCREEN_WIDHT, SCREEN_HEIGHT)
        self.top_label_on = load_image("images/menu/top_label_on.png", SCREEN_WIDHT, SCREEN_HEIGHT)

    def render_item(self):
        self.item_rect = self.items[self.current_item].image.get_rect()
        self.item_rect.center = (SCREEN_WIDHT // 2, SCREEN_HEIGHT // 2)

        self.price_text = text_render(self.items[self.current_item].price)
        self.price_text_rect = self.price_text.get_rect()
        self.price_text_rect.center = (SCREEN_WIDHT // 2, GRID * 18)

        self.name_text = text_render(self.items[self.current_item].name)
        self.name_text_rect = self.name_text.get_rect()
        self.name_text_rect.center = (SCREEN_WIDHT // 2, GRID * 12)

    def draw(self, screen):
        screen.blit(self.menu_page, (0,0))
        screen.blit(self.items[self.current_item].image, self.item_rect)

        if self.items[self.current_item].is_bought:
            screen.blit(self.buttom_label_on, (0, 0))
        else:
            screen.blit(self.buttom_label_off, (0, 0))

        screen.blit(self.price_text, self.price_text_rect)
        screen.blit(self.name_text, self.name_text_rect)
        screen.blit(self.use_text, self.use_text_rect)
        screen.blit(self.buy_text, self.buy_text_rect)

        self.next_button.draw(screen)
        self.previous_button.draw(screen)
        self.use_button.draw(screen)
        self.buy_button.draw(screen)



    def to_next(self):
        if self.current_item != len(self.items) - 1:
            self.current_item += 1
            self.render_item()

    def to_previous(self):
        if self.current_item != 0:
            self.current_item -= 1
            self.render_item()

    def use_item(self):
        if self.items[self.current_item].is_bought:
            self.items[self.current_item].is_using = not self.items[self.current_item].is_using

    def buy (self):
        if self.game.money >= self.items[self.current_item].price:
            self.game.money -= self.items[self.current_item].price
            self.items[self.current_item].is_bought = True

class Button:
    def __init__(self, text, x, y, widht=BUTTON_WIDHT, height=BUTTON_HEIGHT, text_font=font, func=None):
        self.func = func

        self.image = load_image("images/button.png", widht,height) 
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.text_fond = text_font
        self.text = self.text_fond.render(str(text), True, "black")
        self.text_rect = self.text.get_rect()
        self.text_rect.center = self.rect.center

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)
        
    def is_clicked(self, event):
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.func()  

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDHT, SCREEN_HEIGHT))
        pg.display.set_caption("Виртуальный питомец")
        
        with open("save.json", "r", encoding="utf-8") as f:
            data = json.load(f)
        
        self.happiness = data["happiness"]
        self.satiety = data["satiety"]
        self.health = data["health"]
        self.money = data["money"]
        self.coins_ptr_second = data["coins_ptr_second"]

        self.items_on = []

        self.mode = "Main"

        self.background = load_image("images/background.png", SCREEN_WIDHT, SCREEN_HEIGHT)

        self.body = load_image("images/dog.png", DOG_WIDHT, DOG_HEIGHT)
        self.happiness_image = load_image("images/happiness.png", ICON_SIZE, ICON_SIZE)
        self.satiety_image = load_image("images/satiety.png", ICON_SIZE, ICON_SIZE)
        self.health_image = load_image("images/health.png", ICON_SIZE, ICON_SIZE)   
        self.money_image = load_image("images/money.png", ICON_SIZE, ICON_SIZE)

        button_x = SCREEN_WIDHT - BUTTON_WIDHT - GRID
        self.eat_button = Button("еда", button_x, GRID * 9, func=self.food_menu_on)
        self.clothes_button = Button("одежда", button_x, GRID * 10 + BUTTON_HEIGHT, func=self.clothes_menu_on)
        self.play_button = Button("игра", button_x, GRID * 11 + BUTTON_HEIGHT * 2, func=self.game_on)

        self.INCREASE_COINS = pg.USEREVENT + 1
        pg.time.set_timer(self.INCREASE_COINS, 1000)

        self.DECREASE = pg.USEREVENT + 2
        pg.time.set_timer(self.DECREASE, 1000)

        self.clothes_menu = Clothesmenu(self, data["clothes"]) 
        self.food_menu = FoodMenu(self)
        self.mini_game = MiniGame(self)
        
        self.clock = pg.time.Clock()
        self.run()

    def clothes_menu_on(self):
        self.mode = "clothes menu"
        print(self.mode)

    def food_menu_on(self):
        self.mode = "food menu"
        print(self.mode)

    def game_on(self):
        self.mode = "mini game"
        self.mini_game.new_game()
        print(self.mode)

    def event(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.mode == "Game over":
                    data = new_game_data

                else:
                    data = {
                        "happiness": self.happiness,
                        "satiety": self.satiety,
                        "health": self.health,
                        "money": self.money,
                        "coins_ptr_second": self.coins_per_second,
                        "clothes": []
                    }
                    
                    for item in self.clothes_menu.items:
                        data["clothes"].append({"name": item.name,
                                                "price": item.price,
                                                "image": item.file,
                                                "is_using": item.is_using, 
                                                "is_bought": item.is_bought})

                with open('save.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False,indent=4)

                pg.quit()
                exit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.mode = "Main"

            if event.type == self.INCREASE_COINS:
                self.money += self.coins_ptr_second

            if event.type == self.DECREASE:
                chance = random.randint(1, 10)
                if chance <= 5:
                    self.satiety -= 1
                elif chance <= 9:
                    self.happiness -= 1   
                else:
                    self.health -= 1     

            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.money += self.coins_ptr_second

            if self.mode == "Main":
                self.clothes_button.is_clicked(event)
                self.eat_button.is_clicked(event)
                self.play_button.is_clicked(event)

            elif self.mode == "clothes menu":
                self.clothes_menu.next_button.is_clicked(event)
                self.clothes_menu.previous_button.is_clicked(event)
                self.clothes_menu.use_button.is_clicked(event)
                self.clothes_menu.buy_button.is_clicked(event)

            elif self.mode == "food menu":
                self.food_menu.next_button.is_clicked(event)
                self.food_menu.previous_button.is_clicked(event)
                self.food_menu.buy_button.is_clicked(event)

    def update(self):
        if self.mode == "mini game":
            self.mini_game.update()

        if self.happiness <= 0 or self.satiety <= 0 or self.health <= 0:
            self.mode = "Game over"
    
    def draw(self):
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.body,(SCREEN_WIDHT//2 - DOG_WIDHT// 2, GRID * 10))
        self.screen.blit(self.happiness_image, (GRID, GRID))
        self.screen.blit(self.satiety_image, (GRID, GRID + ICON_SIZE))
        self.screen.blit(self.health_image, (GRID, GRID * 2 + ICON_SIZE * 2))
        self.screen.blit(self.money_image, (SCREEN_WIDHT - GRID - ICON_SIZE *2, GRID))

        self.screen.blit(text_render(self.happiness), (GRID + ICON_SIZE, GRID * 4 ))
        self.screen.blit(text_render(self.satiety), (GRID + ICON_SIZE, GRID * 4 + ICON_SIZE ))        
        self.screen.blit(text_render(self.health), (GRID + ICON_SIZE, GRID * 5 + ICON_SIZE * 2 ))

        self.screen.blit(self.money_image, (SCREEN_WIDHT - GRID - ICON_SIZE * 2, GRID))
        self.screen.blit(text_render(self.money), (SCREEN_WIDHT - GRID - ICON_SIZE, GRID * 4))

        self.clothes_button.draw(self.screen)
        self.eat_button.draw(self.screen)
        self.play_button.draw(self.screen)

        self.screen.blit(self.body, (SCREEN_WIDHT // 2 - DOG_WIDHT // 2, GRID * 10))
        for item in self.clothes_menu.items:
            if item.is_using:
                self.screen.blit(item.full_image, (SCREEN_WIDHT // 2 - DOG_WIDHT // 2, GRID * 10))

        if self.mode == "clothes menu":
            self.clothes_menu.draw(self.screen)

        if self.mode == "food menu":
            self.food_menu.draw(self.screen)

        if self.mode == "mini game":
            self.mini_game.draw(self.screen)

        if self.mode == "Game over":
            text = font_maxi.render("ПРОИГРЫШ", True, "red")
            text_rect = text.get_rect(center=(SCREEN_WIDHT // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(text, text_rect)

    def run(self):
        while True:
            self.event()
            self.update()
            self.draw()
            pg.display.flip()
            self.clock.tick(FPS)

if __name__ == "__main__":
    Game()