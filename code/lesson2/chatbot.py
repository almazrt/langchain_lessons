import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_classic.memory import ConversationBufferMemory

# Загружаем переменные окружения из файла .env
load_dotenv()

def main():
    try:
        # Проверяем наличие API ключа
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("Ошибка: Не найден API ключ. Пожалуйста, установите OPENROUTER_API_KEY в переменных окружения или файле .env")
            return
        
        # Инициализируем модель через OpenRouter
        llm = ChatOpenAI(
            model="openai/gpt-3.5-turbo",
            openai_api_key=api_key,
            openai_api_base="https://openrouter.ai/api/v1"
        )
        
        # Инициализируем память
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        
        # Создаем шаблон для чат-бота с учетом истории разговора
        prompt_template = PromptTemplate.from_template(
            "Ты полезный ассистент. Отвечай на вопросы пользователя, учитывая историю разговора.\n\n"
            "История разговора:\n{chat_history}\n\n"
            "Вопрос пользователя: {question}\n"
            "Ответ:"
        )
        
        # Создаем цепочку
        chain = prompt_template | llm
        
        # Пример диалога
        questions = [
            "Какие основные принципы объектно-ориентированного программирования?",
            "Можешь объяснить понятнее про инкапсуляцию?",
            "А как насчет полиморфизма?"
        ]
        
        chat_history = ""
        
        for question in questions:
            print(f"\nПользователь: {question}")
            
            # Получаем ответ
            response = chain.invoke({
                "chat_history": chat_history,
                "question": question
            })
            
            answer = response.content
            print(f"Ассистент: {answer}")
            
            # Обновляем историю разговора
            chat_history += f"Пользователь: {question}\nАссистент: {answer}\n"
        
    except Exception as e:
        print(f"Произошла ошибка при выполнении запроса: {str(e)}")

if __name__ == "__main__":
    main()