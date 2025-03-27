import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class ObserverAgent:
    def __init__(self, logger=None):
        self.logger = logger
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.3,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.setup_chain()
    
    def setup_chain(self):
        prompt_template = """
        Вы - опытный супервизор психологов. Ваша задача - анализировать диалоги 
        между психологом и клиентом, выявляя возможные ошибки, неточности или 
        области для улучшения в работе психолога.

        Обратите особое внимание на:
        1. Соблюдение этических норм
        2. Правильность применения терапевтических техник
        3. Эмпатию и понимание клиента
        4. Четкость и понятность объяснений
        5. Профессиональную грамотность

        Диалог для анализа:
        {dialogue}

        Пожалуйста, проанализируйте этот диалог и укажите:
        1. Основные сильные стороны в работе психолога
        2. Области, требующие улучшения (если есть)
        3. Конкретные рекомендации по улучшению работы
        """
        
        prompt = PromptTemplate(
            input_variables=["dialogue"],
            template=prompt_template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
    
    async def run(self, dialogue):
        """
        Анализирует диалог между психологом и клиентом.
        
        Args:
            dialogue (str): Текст диалога для анализа
            
        Returns:
            str: Результат анализа
        """
        try:
            return await self.chain.arun(dialogue=dialogue)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка в ObserverAgent: {str(e)}")
            return (
                "Произошла ошибка при анализе диалога. "
                f"Техническая информация: {str(e)}"
            ) 