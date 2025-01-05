from contextlib import asynccontextmanager
from app.DBmanager import Base, engine
from app.restaurant.models import Menu, Table
from app.authorization.models import Users, Session, User_Tables_association
from app.authorization.schemas import User_API_in
from app.authorization.roles import Roles
from fastapi import FastAPI
import app.restaurant.repository as rep
from app.restaurant.schemas import Menu_In
from app.restaurant.food_type import food_types
from app.restaurant.repository import add_tables

@asynccontextmanager
async def lifespan_(app: FastAPI):
    #create db
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)
    #     await conn.run_sync(Base.metadata.create_all)
    #
    # borsh = Menu_In(food_name="Суп борщ",
    #                 food_cost=150,
    #                 food_description="Классический украинский борщ с насыщенным вкусом и ароматом. Готовится на основе свеклы, капусты, картофеля и мяса, подается со сметаной и свежей зеленью. Идеальное сочетание сытности и легкости.",
    #                 food_type=food_types.SOUPS,
    #                 food_photo_path="/static/image/menu/borsh.png"
    #                 )
    # pelmeni = Menu_In(food_name="Пельмени",
    #                   food_cost=200,
    #                   food_description="Нежные пельмени ручной лепки с сочной начинкой из отборного мяса. Подаются с маслом, сметаной или уксусом. Традиционное блюдо, которое покоряет своим вкусом и домашним уютом.",
    #                   food_type=food_types.MEAT_DISHES,
    #                   food_photo_path="/static/image/menu/pelmeni.png"
    #                   )
    # grechka = Menu_In(food_name="Гречка с гуляшом",
    #                   food_cost=100,
    #                   food_description="Ароматная рассыпчатая гречка с тушеным мясом в густом соусе. Сытное и полезное блюдо, которое станет отличным выбором для тех, кто ценит простоту и насыщенный вкус.",
    #                   food_type=food_types.MEAT_DISHES,
    #                   food_photo_path="/static/image/menu/grechka.png"
    #                   )
    # medovik = Menu_In(food_name="Торт \"Медовик\"",
    #                   food_cost=150,
    #                   food_description="Нежный медовый торт с тонкими коржами и сливочно-сметанным кремом. Легкий медовый аромат и мягкая текстура делают этот десерт настоящим удовольствием для сладкоежек.",
    #                   food_type=food_types.DESSERTS,
    #                   food_photo_path="/static/image/menu/medovik.png"
    #                   )
    # solyanka = Menu_In(food_name="Суп солянка",
    #                    food_cost=100,
    #                    food_description="Наваристый суп с насыщенным вкусом, приготовленный из смеси мяса, колбасы, соленых огурцов и маслин. Подается с долькой лимона и сметаной. Идеальное блюдо для тех, кто любит яркие и пикантные сочетания.",
    #                    food_type=food_types.SOUPS,
    #                    food_photo_path="/static/image/menu/solyanka.png"
    #                    )
    # olivie = Menu_In(food_name="Салат оливье",
    #                  food_cost=250,
    #                  food_description="Легендарный салат с нежным вкусом, приготовленный из отварного мяса, картофеля, моркови, яиц, огурцов и горошка, заправленный майонезом. Традиционное блюдо для праздников и повседневного стола.",
    #                  food_type=food_types.SNACKS,
    #                  food_photo_path="/static/image/menu/Olivier_salad.png"
    #                  )
    # sashlik = Menu_In(food_name="Шашлык",
    #                   food_cost=550,
    #                   food_description="Сочное мясо, замаринованное в специях и приготовленное на углях. Подается с овощами, зеленью и соусами. Идеальное блюдо для любителей ароматного и насыщенного вкуса.",
    #                   food_type=food_types.MEAT_DISHES,
    #                   food_photo_path="/static/image/menu/sashlik.png"
    #                   )
    # bliny = Menu_In(food_name="Блины",
    #                 food_cost=150,
    #                 food_description="Тонкие, румяные блины с хрустящими краями. Подаются с разнообразными начинками: сметаной, вареньем, медом или икрой. Универсальное блюдо, которое подойдет как для завтрака, так и для десерта.",
    #                 food_type=food_types.DESSERTS,
    #                 food_photo_path="/static/image/menu/bliny.png"
    #                 )
    # uha = Menu_In(food_name="Суп уха",
    #               food_cost=250,
    #               food_description="Ароматная рыбная уха, приготовленная из свежей рыбы с добавлением картофеля, моркови и специй. Легкий и наваристый суп, который порадует любителей рыбных блюд.",
    #               food_type=food_types.SOUPS,
    #               food_photo_path="/static/image/menu/uha.png"
    #               )
    # plov = Menu_In(food_name="Плов",
    #                food_cost=350,
    #                food_description="Ароматный плов с нежным мясом, рисом и специями. Традиционное блюдо восточной кухни, которое сочетает в себе насыщенный вкус и сытность. Подается с овощами и зеленью.",
    #                food_type=food_types.MEAT_DISHES,
    #                food_photo_path="/static/image/menu/plov.png"
    #                )
    # pivo = Menu_In(food_name="Пиво светлое",
    #                food_cost=150,
    #                food_description="Освежающий золотистый напиток с тонким ароматом хмеля и легкой горчинкой. Идеально сбалансированный вкус, который подчеркивает свежесть и насыщенность. Отлично сочетается с закусками, мясными блюдами и дружескими посиделками.",
    #                food_type=food_types.DRINKS,
    #                food_photo_path="/static/image/menu/pivo.png"
    #                )
    # black_tea = Menu_In(food_name="Чай черный",
    #                     food_cost=50,
    #                     food_description="Насыщенный черный чай с глубоким ароматом и терпким вкусом. Идеальный напиток для утреннего пробуждения или вечернего отдыха. Подается горячим, с лимоном, сахаром или молоком, чтобы подчеркнуть его богатый вкус.",
    #                     food_type=food_types.DRINKS,
    #                     food_photo_path="/static/image/menu/black_tea.png"
    #                     )
    # await rep.add_food_to_menu(borsh)
    # await rep.add_food_to_menu(pelmeni)
    # await rep.add_food_to_menu(grechka)
    # await rep.add_food_to_menu(medovik)
    # await rep.add_food_to_menu(solyanka)
    # await rep.add_food_to_menu(olivie)
    # await rep.add_food_to_menu(sashlik)
    # await rep.add_food_to_menu(bliny)
    # await rep.add_food_to_menu(uha)
    # await rep.add_food_to_menu(plov)
    # await rep.add_food_to_menu(pivo)
    # await rep.add_food_to_menu(black_tea)
    #
    # await add_tables()

    yield
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)