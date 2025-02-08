from googletrans import Translator
import googletrans
import asyncio
class EngToArabic:
	def __init__(self):
		self.translator = Translator()
	async def translate(self, text):
		translation = await self.translator.translate(text, dest='ar')
		return translation.text
	
class ArabicToEng:
	def __init__(self):
		self.translator = Translator()
	async def translate(self, text):
		translation = await self.translator.translate(text, dest='en')
		return translation.text
# print(googletrans.LANGUAGES)
# import asyncio

# async def translate_text():
# 	translation = await translator.translate("Hello", dest='ar')
# 	print(translation.text)

# asyncio.run(translate_text())
