import allure
import pytest
from pages.home_page import HomePage
from data.test_data import FAQ_DATA


@allure.epic("Тестирование сервиса 'Яндекс.Самокат'")
@allure.feature("Раздел 'Вопросы о важном'")
class TestFaq:
    @pytest.mark.faq
    @allure.title("Проверка соответствия ответа вопросу")
    @pytest.mark.parametrize("question, expected_answer", FAQ_DATA)
    def test_faq_answers(self, driver, question, expected_answer):
        home_page = HomePage(driver)
        home_page.scroll_to_faq()
        home_page.click_question(question)
        
        assert home_page.is_answer_visible(question), f"Ответ на вопрос '{question}' не появился"
        
        actual_answer = home_page.get_answer_text(question)
        assert actual_answer == expected_answer