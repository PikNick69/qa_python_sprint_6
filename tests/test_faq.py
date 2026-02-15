import allure
import pytest
from pages.home_page import HomePage
from data.test_data import FAQ_DATA


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Раздел 'Вопросы о важном'")
class TestFaq:

    @pytest.mark.faq
    @allure.title("Проверка соответствия ответа вопросу")
    @allure.description("Тест проверяет, что при клике на вопрос открывается правильный ответ")
    @pytest.mark.parametrize("question, expected_answer", FAQ_DATA)
    def test_faq_answers(self, driver, question, expected_answer):
        home_page = HomePage(driver)
        
        with allure.step("Скролл до раздела с вопросами"):
            home_page.scroll_to_faq()

        with allure.step(f"Клик по вопросу: {question}"):
            home_page.click_question(question)
        
        with allure.step("Получение текста ответа"):
            actual_answer = home_page.get_answer_text(question)
        
        with allure.step("Проверка соответствия ответа"):
            assert actual_answer == expected_answer, \
                f"Ожидаемый ответ: {expected_answer}, Фактический: {actual_answer}"