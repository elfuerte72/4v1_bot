import os
from langchain_openai import ChatOpenAI
from langchain.agents import ZeroShotAgent, AgentExecutor, Tool
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from search_tool import get_search_tool

class TherapistAgent:
    def __init__(self, logger=None):
        self.logger = logger
        self.llm = ChatOpenAI(
            model="gpt-4",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY")
        )
        self.tools = [get_search_tool()]
        self.setup_agent()
        
    def setup_agent(self):
        tools_info = "\n".join([f"{tool.name}: {tool.description}" 
                               for tool in self.tools])
        
        prompt_template = """
        Вы - профессиональный психолог-консультант с обширным опытом в терапии. 
        Ваша задача - помогать клиентам, проявляя эмпатию, задавая правильные 
        вопросы и предлагая подходящие методики.
        
        У вас есть доступ к следующим инструментам:
        {tools}
        
        Используйте инструмент поиска только когда клиент явно запрашивает 
        фактическую информацию, упоминает исследования, методики, статьи, 
        научные факты или когда вам нужно проверить конкретную информацию 
        перед ответом. В остальных случаях отвечайте на основе своих знаний 
        и опыта как терапевт.
        
        Формат взаимодействия:
        Вопрос: вопрос клиента
        Мысли: размышления о том, как лучше всего ответить или какой инструмент 
               использовать
        Действие: имя используемого инструмента
        Данные действия: информация, полученная от инструмента
        Наблюдение: результат использования инструмента
        Ответ: ваш окончательный ответ клиенту
        
        История беседы:
        {chat_history}
        
        Начнем!
        Вопрос: {input}
        {agent_scratchpad}
        """
        
        prompt = PromptTemplate(
            input_variables=["input", "chat_history", "agent_scratchpad", "tools"],
            template=prompt_template
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        llm_chain = LLMChain(
            llm=self.llm,
            prompt=prompt
        )
        
        agent = ZeroShotAgent(
            llm_chain=llm_chain,
            tools=self.tools,
            verbose=True
        )
        
        self.agent_executor = AgentExecutor.from_agent_and_tools(
            agent=agent,
            tools=self.tools,
            memory=self.memory,
            verbose=True,
            handle_parsing_errors=True,
            max_iterations=3
        )
    
    def should_use_search(self, user_message):
        """
        Определяет, нужно ли использовать поиск в интернете для текущего сообщения.
        """
        search_keywords = [
            "статья", "исследование", "факт", "методика", "метод", 
            "техника", "что говорит наука", "научно доказано", 
            "исследования показывают", "согласно исследованиям",
            "ссылка", "источник", "проверь"
        ]
        
        return any(keyword in user_message.lower() for keyword in search_keywords)
    
    async def generate_response(self, user_message, dialog_history=None):
        try:
            if dialog_history is None:
                dialog_history = []
                
            if dialog_history:
                for entry in dialog_history[-5:]:
                    if 'user_message' in entry and entry['user_message']:
                        self.memory.chat_memory.add_user_message(
                            entry['user_message']
                        )
                    if 'bot_message' in entry and entry['bot_message']:
                        self.memory.chat_memory.add_ai_message(
                            entry['bot_message']
                        )
            
            use_search = self.should_use_search(user_message)
            
            if use_search:
                response = await self.agent_executor.arun(input=user_message)
            else:
                response = await self.llm_chain.arun(
                    input=user_message,
                    chat_history=self.format_history(dialog_history)
                )
                
            return response
        except Exception as e:
            if self.logger:
                self.logger.error(f"Ошибка в TherapistAgent: {str(e)}")
            return (
                "Извините, произошла ошибка при обработке вашего запроса. "
                f"Пожалуйста, попробуйте еще раз. Техническая информация: {str(e)}"
            )
    
    def format_history(self, dialog_history):
        """Форматирует историю диалога для использования в промпте."""
        if not dialog_history:
            return ""
        
        formatted = []
        for entry in dialog_history[-5:]:  # Берем последние 5 сообщений
            if 'user_message' in entry:
                formatted.append(f"Клиент: {entry['user_message']}")
            if 'bot_message' in entry:
                formatted.append(f"Психолог: {entry['bot_message']}")
        
        return "\n".join(formatted) 