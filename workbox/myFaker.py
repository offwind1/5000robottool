from faker.providers.lorem.zh_CN import Provider as zh_CN_lorem
from faker.providers.person.zh_CN import Provider as zh_CN_person
from faker.generator import Generator
from faker.config import *

faker = Generator()
faker.add_provider(zh_CN_person)
faker.add_provider(zh_CN_lorem)
