import os
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate


class CorrectorAgent:
    def __init__(self, logger=None):
        self.logger = logger
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.4,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.setup_chain()
    
    def setup_chain(self):
        prompt_template = """
        Вы - эксперт по улучшению промптов для языковых моделей. Ваша задача - 
        обновить промпт психолога-консультанта на основе анализа его работы.

        Текущий промпт психолога:
        {old_prompt}

        Анализ работы психолога:
        {analysis}

        Пожалуйста, создайте обновленную версию промпта, которая:
        1. Сохранит все сильные стороны текущего промпта
        2. Исправит выявленные проблемы
        3. Добавит конкретные инструкции по улучшению работы
        4. Сделает акцент на этичности и профессионализме
        5. Сохранит ясность и четкость инструкций

        Обновленный промпт должен быть конкретным, практичным и эффективным.
        """
        
        prompt = PromptTemplate(
            input_variables=["old_prompt", "analysis"],
            template=prompt_template
        )
        
        self.chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
    
    async def run(self, old_prompt, analysis):
        """
        Обновляет промпт психолога на основе анализа его работы.
        
        Args:
            old_prompt (str): Текущий промпт психолога
            analysis (str): Анализ работы психолога
            
        Returns:
            str: Обновленный промпт
        """
        try:
            return await self.chain.arun(
                old_prompt=old_prompt,
                analysis=analysis
            )
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка в CorrectorAgent: {str(e)}")
            return (
                "Произошла ошибка при обновлении промпта. "
                f"Техническая информация: {str(e)}"
            ) 