from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

def scrape_glassdoor_salary():
    url = "https://www.glassdoor.com.br/Salários/cientista-de-dados-salário-SRCH_KO0,18.htm"
    credentials = {
        "email": "19f266b11f@emaily.pro",
        "password": ""
    }

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 20)
    resultados = []

    try:
        driver.get(url)
        time.sleep(0.5) 
        # Clica no botão "Entrar"
        entrar_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@aria-label='sign in' and .//span[contains(text(), 'Entrar')]]"
        )))
        entrar_btn.click()
        time.sleep(0.5) 
        # Aguarda o campo de e-mail no modal
        email_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@id='modalUserEmail']"
        )))
        email_input.clear()
        email_input.send_keys(credentials["email"])
        time.sleep(0.5) 
        # Clica em "Continuar com e‑mail"
        continuar_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@data-test='continue-with-email-modal' and .//span[contains(text(), 'Continuar com e‑mail')]]"
        )))
        continuar_btn.click()
        time.sleep(1.5)  # Aguarda o modal de senha aparecer
        # Aguarda o campo de senha aparecer
        password_input = wait.until(EC.presence_of_element_located((
            By.XPATH, "//input[@id='modalUserPassword']"
        )))
        password_input.clear()
        password_input.send_keys(credentials["password"])
        time.sleep(0.5) 
        # Clica no botão "Entrar" após digitar a senha
        entrar_final_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@type='submit' and contains(@class, 'Button') and .//span[text()='Entrar']]"
        )))
        entrar_final_btn.click()
        time.sleep(1.5)  # Aguarda o login ser processado
        # Aguarda redirecionar para a página de salários
        driver.get(url)
        time.sleep(0.5) 
        # Filtro de experiência
        exp_btn = wait.until(EC.element_to_be_clickable((
            By.XPATH, "//button[@aria-label='Experiência']"
        )))
        exp_btn.click()
        time.sleep(0.5) 
        opcoes = ['0 a 1 ano', '1 a 3 anos', '4 a 6 anos', '7 a 9 anos', '10 a 14 anos', 'Mais de 15 anos']
        for experiencia in opcoes:
            # Abre o dropdown novamente
            exp_btn = wait.until(EC.element_to_be_clickable((
                By.XPATH, "//button[@aria-label='Experiência']"
            )))
            exp_btn.click()
            time.sleep(0.5)  # Aguarda o dropdown abrir
            # Aguarda e clica na opção atual
            opcao_element = wait.until(EC.element_to_be_clickable((
                By.XPATH, f"//div[@role='option' and .//span[text()='{experiencia}']]"
            )))
            opcao_element.click()

            time.sleep(2)  # Aguarda atualização da página

            try:
                salary_span = wait.until(EC.presence_of_element_located((
                    By.XPATH, "//span[contains(@class, 'TotalPayRange_StyledAverageComp')]"
                )))
                salario = salary_span.text.strip()
            except:
                salario = "Não encontrado"

            print(f"Experiência: {experiencia} | Salário: {salario}")
            resultados.append({"experiencia": experiencia, "salario": salario})

        # Salva os dados no CSV
        with open("salarios.csv", mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=["experiencia", "salario"])
            writer.writeheader()
            for linha in resultados:
                writer.writerow(linha)

        print("\n✅ Todos os dados foram salvos no arquivo 'salarios.csv'.")

    finally:
        driver.quit()

if __name__ == "__main__":
    scrape_glassdoor_salary()