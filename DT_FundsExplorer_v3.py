import pandas as pd
import numpy as np
from datetime import date
from time import sleep
import os
from io import StringIO

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
##---------------------------------------------------------------------------------
def scrape_fundsexplorer_selenium():
    """
    Função de scraping usando Selenium
    """
    
    print("="*46)
    print(" - Iniciando scraping do FundsExplorer.com ...")
    print("="*46)

    # Configura Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    # chrome_options.add_argument('--headless=new')  # Descomente para modo headless
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)
    
    try:
        # Acessa a página
        print("🌐 Acessando FundsExplorer ranking")
        driver.get("https://www.fundsexplorer.com.br/ranking")
        sleep(3)
        
        # Fecha popup de cookies
        print("🍪 Fechando popup de cookies...")
        try:
            cookie_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="hs-eu-confirmation-button"]'))
            )
            cookie_button.click()
            print("✅ Cookie aceito!")
            sleep(2)
        except TimeoutException:
            print("⚠️  Botão de cookie não encontrado")
        
        # Fecha popup de propaganda
        print("🚫 Tentando fechar popup de propaganda...")
        try:
            iframe_element = driver.find_element(By.XPATH, "//iframe[@title='Popup CTA']")
            driver.switch_to.frame(iframe_element)
            close_button = driver.find_element(By.XPATH, "/html/body/div/div[1]")
            close_button.click()
            driver.switch_to.default_content()
            print("✅ Popup fechado!")
            sleep(2)
        except (NoSuchElementException, TimeoutException):
            print("⚠️  Popup não encontrado - FECHE MANUALMENTE se aparecer")
            driver.switch_to.default_content()
            sleep(5)
        
        # Rola a página
        print(" - Rolando a página...")
        driver.execute_script("window.scrollBy(0, 500);")
        sleep(2)
        
        # Seleciona todas as colunas
        print(" - Selecionando todas as colunas...")
        colunas_selecionadas = False
        try:
            columns_button = wait.until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="colunas-ranking__select-button"]'))
            )
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", columns_button)
            sleep(0.5)
            try:
                columns_button.click()
            except Exception:
                driver.execute_script("arguments[0].click();", columns_button)
            sleep(2)

            # Tenta localizar a opção "selecionar todas" de várias formas, pois o
            # XPath absoluto (/html/body/div[7]/...) é frágil e quebra se a
            # estrutura da página mudar (ex: outro popup abriu antes e deslocou os índices)
            all_columns_option = None
            candidatos_xpath = [
                '/html/body/div[7]/div[1]/div/div[2]/div[2]/ul/li[1]/label',
                "//ul[contains(@class,'colunas') or contains(@id,'colunas')]//li[1]/label",
                "//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'selecionar todas')]",
                "//label[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'todas')]",
            ]
            for xp in candidatos_xpath:
                try:
                    all_columns_option = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, xp))
                    )
                    if all_columns_option:
                        break
                except TimeoutException:
                    continue

            if all_columns_option is None:
                raise TimeoutException("Não foi possível localizar a opção 'selecionar todas as colunas' com nenhum dos XPaths testados")

            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", all_columns_option)
            sleep(0.5)
            try:
                all_columns_option.click()
            except Exception:
                # Fallback: alguns overlays interceptam cliques normais do Selenium
                driver.execute_script("arguments[0].click();", all_columns_option)
            sleep(3)
            print("✅ Todas as colunas selecionadas!")
            colunas_selecionadas = True
        except TimeoutException as e:
            print(f"⚠️  Erro ao selecionar colunas: {e}")
            driver.save_screenshot("error_screenshot_colunas.png")
            print("📸 Screenshot do estado da tela salvo em error_screenshot_colunas.png para depuração")

        if not colunas_selecionadas:
            # Não interrompe o scraping (a tabela padrão ainda tem dados úteis),
            # mas sinaliza claramente que apenas as colunas padrão serão extraídas
            print("⚠️  Prosseguindo apenas com as colunas padrão da tabela (nem todas as colunas foram selecionadas)")
        
        # Extrai a tabela
        print(" - Extraindo dados da tabela...")
        html_str = driver.page_source
        tabelas_html = pd.read_html(StringIO(html_str))
        
        if len(tabelas_html) == 0:
            raise Exception("❌ Nenhuma tabela encontrada na página!")
        
        df = tabelas_html[0]
        print(f"✅ Tabela extraída! {len(df)} fundos encontrados")
        
        return df
        
    except Exception as e:
        print(f"❌ Erro durante o scraping: {e}")
        driver.save_screenshot("error_screenshot_selenium.png")
        print("📸 Screenshot do erro salvo")
        raise
        
    finally:
        print("🔒 Fechando navegador...")
        driver.quit()
##---------------------------------------------------------------------------------

df = pd.DataFrame()
try:
    df = scrape_fundsexplorer_selenium()
    print("\n🎉 Sucesso! Dados extraídos com Selenium!")
except Exception as e:
    print(f"\n💥 Falha no scraping: {e}")
##---------------------------------------------------------------------------------
def converter_valor(x):
    """Converte valores do formato brasileiro para float"""
    if pd.isna(x) or x == 'N/A':
        return np.nan
    x = str(x)
    if 'R$' in x : x = x.replace('R$', '').strip()
    if ',' in x:  # formato brasileiro
        x = x.replace('.', '').replace(',', '.')
        return round(float(x),2)
    else:  # sem vírgula → interpretar como centavos implícitos
        return round(float(x) / 100,2)
    
def converter_porcento(x):
    """Converte valores em porcentagem para float"""
    if pd.isna(x) or x == 'N/A':
        return np.nan
    x = str(x).strip()
    x = x.replace('%', '').replace(' a.a', '').strip()  # remove % e A.A
    if not x:
        return np.nan
    if ',' in x:  # formato brasileiro
        x = x.replace('.', '').replace(',', '.')

    return float(x) #/ 100    
    
##---------------------------------------------------------------------------------
# Valida se as colunas esperadas estão presentes antes de processar. Se a etapa
# de "selecionar todas as colunas" falhou no scraping, df só terá as colunas
# padrão da tabela e as linhas abaixo dariam KeyError de forma confusa.
colunas_esperadas = (
    ['Fundos', 'Setor', 'Preço Atual (R$)', 'Último Dividendo', 'Liquidez Diária (R$)',
     'Volatilidade', 'VPA', 'P/VP', 'Num. Cotistas', 'P/VPA'] +
    ['Dividend Yield', 'DY (3M) Acumulado', 'DY (6M) Acumulado', 'DY (12M) Acumulado',
     'DY (3M) média', 'DY (6M) média', 'DY (12M) média', 'DY Ano',
     'Variação Preço', 'Rentab. Período', 'Rentab. Acumulada',
     'DY Patrimonial', 'Variação Patrimonial', 'Rentab. Patr. Período', 'Rentab. Patr. Acumulada',
     'Tax. Gestão', 'Tax. Performance', 'Tax. Administração']
)
colunas_faltando = [c for c in colunas_esperadas if c not in df.columns]
if colunas_faltando:
    print("❌ Colunas esperadas ausentes na tabela extraída — provavelmente a seleção")
    print("   de 'todas as colunas' falhou no site durante o scraping.")
    print(f"   Colunas faltando ({len(colunas_faltando)}): {colunas_faltando}")
    print(f"   Colunas disponíveis: {df.columns.tolist()}")
    raise KeyError(
        "Tabela extraída não contém todas as colunas esperadas. "
        "Verifique error_screenshot_colunas.png e ajuste os seletores da etapa "
        "'Selecionando todas as colunas'."
    )

estrigues = ['Fundos' , 'Setor']
for x in estrigues : df[x] = df[x].astype('string')

reais = ['Preço Atual (R$)','Último Dividendo', 'Liquidez Diária (R$)', 'Volatilidade' , 'VPA' , 'P/VP']
for x in reais : df[x] = df[x].apply(converter_valor)

porcentagens = ['Dividend Yield', 'DY (3M) Acumulado', 'DY (6M) Acumulado', 'DY (12M) Acumulado', 'DY (3M) média', 'DY (6M) média', 
                'DY (12M) média', 'DY Ano' ,
                'Variação Preço' , 'Rentab. Período' , 'Rentab. Acumulada' ,
                'DY Patrimonial' , 'Variação Patrimonial' , 'Rentab. Patr. Período' , 'Rentab. Patr. Acumulada' ,
                'Tax. Gestão' , 'Tax. Performance' , 'Tax. Administração'    ]
for col in porcentagens : 
    df[col] = df[col].apply(converter_porcento)
    if 'Tax.' in col : df.rename(columns={ col : col+' (%aa)'}, inplace=True)
    else : df.rename(columns={ col : col+' (%)'}, inplace=True)
    
df['Num. Cotistas'] = df['Num. Cotistas'].str.replace('.', '', regex=False).astype('Int64')

df['P/VPA'] = df['P/VPA']/100
#df = df.replace([np.inf, -np.inf], 'N/A')
#df = df.fillna('N/A')

df = df.replace([np.inf, -np.inf], np.nan)  # normaliza inf → NaN primeiro
with pd.option_context('future.no_silent_downcasting', True):
    df = df.astype(object).fillna('N/A')     # converte tudo pra object, aí aceita string
##---------------------------------------------------------------------------------
def dadosInfra () :

    print("="*46)
    print(" - Iniciando scraping do Investidor10.com ...")
    

    # Configura Chrome
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--start-maximized')
    chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    # chrome_options.add_argument('--headless=new')  # Descomente para modo headless
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.implicitly_wait(10)
    wait = WebDriverWait(driver, 20)
    
 
    xpath1='//*[@id="table-indicators"]/div[12]/div[2]/div/span'
    xpath2='//*[@id="table-indicators"]/div[14]/div[2]/div'
    xpath3='//*[@id="cards-ticker"]/div[2]/div[2]/div/span'

    print(" = scraping JURO11 ")

    # driver.get("https://data.anbima.com.br/fundos/627127")
    driver.get("https://investidor10.com.br/fiis/juro11/")

    sleep(3)

    juro11_vpa = converter_valor(driver.find_element(By.XPATH,xpath1).text)
    juro11_div = converter_valor(driver.find_element(By.XPATH,xpath2).text)
    juro11_dy = converter_porcento(driver.find_element(By.XPATH,xpath3).text)
    

    print(" = scraping BIDB11 ")

    # driver.get("https://data.anbima.com.br/fundos/617350")
    driver.get("https://investidor10.com.br/fiis/bidb11/")
    sleep(3)

    bidb11_vpa = converter_valor(driver.find_element(By.XPATH,xpath1).text)
    bidb11_div = converter_valor(driver.find_element(By.XPATH,xpath2).text)
    bidb11_dy = converter_porcento(driver.find_element(By.XPATH,xpath3).text)
    
    print(" = scraping CPTI11 ")

    # driver.get("https://data.anbima.com.br/fundos/617350")
    driver.get("https://investidor10.com.br/fiis/cpti11/")
    sleep(3)

    cpti11_vpa = converter_valor(driver.find_element(By.XPATH,xpath1).text)
    cpti11_div = converter_valor(driver.find_element(By.XPATH,xpath2).text)
    cpti11_dy = converter_porcento(driver.find_element(By.XPATH,xpath3).text)

    driver.close()
    print("="*46)

    return juro11_vpa,juro11_div,juro11_dy,bidb11_vpa, bidb11_div, bidb11_dy ,cpti11_vpa , cpti11_div , cpti11_dy
##---------------------------------------------------------------------------------


# print(" ====== Escreve na planilha")
# # from DT_atualiza_settings import *
today = date.today().strftime("%d/%m/%Y")

import gspread
from google.oauth2.service_account import Credentials

scope = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    # "/home/yair/GHub/Finance-playground/carteira-328314-2248cd9489bb.json",
    "/home/yair/GHub/Finance-playground/carteira-328314-d38dcc8ee3e4.json",
    scopes=scope
)

gc = gspread.authorize(creds)

try:
    planilha = gc.open('Investimentos')
    pagina = planilha.worksheet("FundsExp")
    # pagina = planilha.worksheet("Cópia de FundsExp")
    pagina.clear()

    pagina.update(range_name= 'a1',values= [[today]])
    
    # Preparar dados para envio
    dados_para_envio = [df.columns.values.tolist()] + df.values.tolist()
    
    # Debug: mostrar os primeiros valores para verificar se há problemas
    print("Primeiras linhas dos dados:")
    for i, linha in enumerate(dados_para_envio[:3]):  # Mostra apenas as 3 primeiras linhas
        print(f"Linha {i}: {linha[:5]}...")  # Mostra apenas os primeiros 5 valores
    
    pagina.update(range_name='a2', values=dados_para_envio)
    
    print(" ====== Funds Explorer terminou com sucesso")
    
except Exception as e:
    print(f" ====== Erro ao escrever na planilha: {e}")
    print(" ====== Salvando dados localmente como backup")
    df.to_csv(f'backup_fundsexplorer_{today.replace("/", "_")}.csv', index=False)



print(" ====== FI-Infra ===== ")

try:
    juro11_vpa,juro11_div,juro11_dy,bidb11_vpa, bidb11_div, bidb11_dy ,cpti11_vpa , cpti11_div , cpti11_dy = dadosInfra()

    print(" ====== Escreve na planilha")

    planilha = gc.open('Investimentos')
    pagina = planilha.worksheet('FundsExp')
    # pagina = planilha.worksheet("Cópia de FundsExp")

    pagina.update(range_name='b1',values= [["juro11 (VPA,Prov,DY)"]])
    pagina.update(range_name='c1',values= [[juro11_vpa]])
    pagina.update(range_name='d1',values= [[juro11_div]])
    pagina.update(range_name='e1',values= [[juro11_dy]])
    pagina.update(range_name='f1',values= [["bidb11 (VPA,Prov,DY)"]])
    pagina.update(range_name='g1',values= [[bidb11_vpa]])
    pagina.update(range_name='h1',values= [[bidb11_div]])
    pagina.update(range_name='i1',values= [[bidb11_dy]])
    pagina.update(range_name='j1',values= [["cpti11 (VPA,Prov,DY)"]])
    pagina.update(range_name='k1',values= [[cpti11_vpa]])
    pagina.update(range_name='l1',values= [[cpti11_div]])
    pagina.update(range_name='m1',values= [[cpti11_dy]])

    print(" ====== FI-Infra Terminou")
    
except Exception as e:
    print(f" ====== Erro na seção FI-Infra: {e}")

# finally:
#     # Certificar que o driver é fechado mesmo em caso de erro
#     try:
#         driver.close()
#     except:
#         pass

