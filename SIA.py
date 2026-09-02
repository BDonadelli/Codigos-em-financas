
print("==============================================")
print("============== nova atualização ==============")
print("====== Status Invest e Fundamentus ===========")

import os
from time import sleep
from datetime import date
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service


# Configurações
data_path = os.path.join(os.getcwd(), "data")
os.makedirs(data_path, exist_ok=True)

# Configurar Chrome
service = Service(ChromeDriverManager().install())
opts = webdriver.ChromeOptions()

# Perfil de Chrome persistente (fixo em ./chrome_profile): mantém cookies
# entre execuções — inclui o cookie de sessão que o Cloudflare emite depois
# que você resolve o desafio "Confirme que é humano" manualmente. Sem isso,
# toda execução parte do zero e o Cloudflare desconfia de novo.
perfil_dir = os.path.join(os.getcwd(), "chrome_profile")
os.makedirs(perfil_dir, exist_ok=True)

# Limpa locks de execuções anteriores que não fecharam o Chrome direito
# (comum com detach=True: se o script travou/foi encerrado antes do
# driver.quit(), o Chrome fica aberto e o lock permanece). Sem isso, a
# próxima abertura com o mesmo perfil recusa a conexão do Selenium.
for _lockfile in ('SingletonLock', 'SingletonCookie', 'SingletonSocket'):
    _caminho_lock = os.path.join(perfil_dir, _lockfile)
    if os.path.exists(_caminho_lock) or os.path.islink(_caminho_lock):
        try:
            os.remove(_caminho_lock)
            print(f'  Removido lock de execução anterior: {_lockfile} '
                  f'(se você tinha uma janela do Chrome desse perfil aberta '
                  f'de propósito, feche-a antes de rodar de novo)')
        except OSError:
            pass
opts.add_argument(f'--user-data-dir={perfil_dir}')
opts.add_experimental_option("detach", True)
opts.add_experimental_option("prefs", {
    "download.default_directory": data_path,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "safebrowsing.enabled": True,
    # Bloqueia imagens e fontes para carregar mais rápido
    "profile.managed_default_content_settings.images": 2,
    "profile.managed_default_content_settings.fonts": 2,
})

# --- Anti-detecção básica ---
# Selenium "puro" deixa marcas óbvias (navigator.webdriver=true, flag de
# automação na barra do Chrome) que sites com proteção anti-bot usam para
# identificar tráfego automatizado e silenciosamente quebrar funcionalidades
# (sem lançar timeout — a página carrega, só o botão não funciona de verdade).
opts.add_experimental_option("excludeSwitches", ["enable-automation"])
opts.add_experimental_option("useAutomationExtension", False)
opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_argument(
    'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
)

# Não espera a página carregar 100% — evita o timeout do Selenium
# O script aguarda os elementos específicos que precisa via WebDriverWait
opts.page_load_strategy = 'none'

# Argumentos que reduzem consumo e aumentam velocidade
opts.add_argument('--disable-extensions')
opts.add_argument('--disable-gpu')
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.add_argument('--blink-settings=imagesEnabled=false')

# Abrir navegador
service_obj = Service(
    ChromeDriverManager().install(),
    # Aumenta o timeout interno do ChromeDriver para 300s
    service_args=['--timeout=300']
)
driver = webdriver.Chrome(service=service_obj, options=opts)

# Sobrescreve navigator.webdriver antes de qualquer script da página rodar
# (o site pode checar isso em JS para decidir bloquear/ocultar funcionalidades)
driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
})

# Timeout global de página (fallback, em ms)
driver.set_page_load_timeout(180)
driver.set_script_timeout(60)

# WebDriverWait com 30s para elementos (página pode ser lenta)
wait = WebDriverWait(driver, 30)

print('====== Abrindo página')
try:
    driver.get('https://statusinvest.com.br/acoes/busca-avancada')
except TimeoutException:
    # Com page_load_strategy='none' isso não deve ocorrer,
    # mas se ocorrer com outra estratégia, continua mesmo assim
    print('  Timeout no carregamento — continuando (page_load_strategy=none)')

# Aguarda o botão de busca estar presente como sinal de que o DOM está pronto
print('====== Aguardando DOM carregar')
try:
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//div/button[contains(@class,"find")]'))
    )
    print('  DOM pronto')
except TimeoutException:
    print('  ATENÇÃO: botão de busca não encontrado em 60s. A página pode não ter carregado.')

sleep(2)


def fechar_popups():
    """
    Tenta fechar qualquer popup/propaganda visível na página.
    Cobre múltiplos seletores possíveis para ser robusto a mudanças no site.
    """
    seletores = [
        # Botão de fechar por classe comum de modais
        (By.CSS_SELECTOR, '.popup-fixed .btn-close'),   # combina dois identificadores únicos — a div pai popup-fixed e o botão btn-close 
        (By.CSS_SELECTOR, '.modal.open .modal-close'),
        (By.CSS_SELECTOR, '.modal.open button.btn-flat'),
        # Botão de fechar por ícone "close" dentro de modal aberto
        (By.XPATH, '//div[contains(@class,"modal") and contains(@style,"display: block")]//button[.//i[text()="close"]]'),
        (By.XPATH, '//div[contains(@class,"modal") and contains(@style,"display: block")]//i[text()="close"]'),
        # XPath original do script (div[16] — pode mudar conforme a página)
        (By.XPATH, '/html/body/div[16]/div/div/div[1]/button/i'),
        (By.XPATH, '/html/body/div[15]/div/div/div[1]/button/i'),
        (By.XPATH, '/html/body/div[17]/div/div/div[1]/button/i'),
        # Overlay/backdrop genérico
        (By.CSS_SELECTOR, '#plano-invalido-modal .modal-close'),
        (By.CSS_SELECTOR, '#main-modal .modal-close'),
    ]

    fechou = False
    for by, seletor in seletores:
        try:
            elemento = driver.find_element(by, seletor)
            if elemento.is_displayed():
                elemento.click()
                print(f'  Popup fechado com seletor: {seletor}')
                sleep(1)
                fechou = True
                break
        except (NoSuchElementException, ElementClickInterceptedException):
            continue

    if not fechou:
        # Fallback genérico: procura por heurística visual, em vez de
        # seletor fixo — cobre popups promocionais que o site troca com
        # frequência (o "X" pequeno no canto do modal, como o que aparece
        # depois da busca oferecendo login pra salvar filtros).
        fechou = fechar_popup_por_heuristica()

    if not fechou:
        # Última tentativa: pressionar ESC para fechar qualquer modal aberto
        try:
            from selenium.webdriver.common.keys import Keys
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.ESCAPE)
            sleep(0.5)
        except Exception:
            pass

    return fechou


def fechar_popup_por_heuristica():
    """
    Procura, via JS, qualquer elemento pequeno e visível cujo texto seja
    um ícone de fechar ("×"/"X") ou cuja classe contenha "close", e clica
    nele. Mais robusto que seletores fixos porque não depende do nome/id
    exato do popup do momento (ex.: "popup-lojinha-aon-08/2026" hoje,
    outro nome amanhã) — só do padrão visual do botão de fechar.
    """
    js = """
    const candidatos = Array.from(document.querySelectorAll('button, i, span, div, svg, a'));
    for (const el of candidatos) {
        const texto = (el.textContent || '').trim();
        const cls = (el.className || '').toString().toLowerCase();
        const rect = el.getBoundingClientRect();
        const visivel = rect.width > 0 && rect.height > 0 && rect.top >= 0 && rect.top < window.innerHeight;
        if (!visivel) continue;
        const pareceFechar = texto === '\\u00d7' || texto.toUpperCase() === 'X'
            || cls.includes('close') || cls.includes('btn-close');
        // ícone de fechar é pequeno — evita clicar em blocos grandes de texto/layout
        const pequeno = rect.width < 80 && rect.height < 80;
        if (pareceFechar && pequeno) {
            el.click();
            return el.outerHTML.slice(0, 150);
        }
    }
    return null;
    """
    try:
        resultado = driver.execute_script(js)
        if resultado:
            print(f'  Popup fechado via heurística (elemento: {resultado}...)')
            sleep(1)
            return True
    except Exception as e:
        print(f'  Heurística de fechar popup falhou: {e}')
    return False


def pagina_e_desafio_cloudflare():
    """
    Detecta a página de verificação "Confirme que é humano" do Cloudflare
    Turnstile. Usada para pausar e pedir resolução manual, em vez de
    tentar contornar (o que não fazemos de propósito — é uma proteção
    de segurança colocada pelo site).
    """
    try:
        titulo = (driver.title or '').lower()
        origem = driver.page_source.lower()
        return (
            'um momento' in titulo
            or 'verificação de segurança' in origem
            or ('cloudflare' in origem and 'confirme que' in origem)
        )
    except Exception:
        return False


def aguardar_resolucao_manual_cloudflare(timeout_segundos=180):
    """
    Pausa a execução e pede pra você resolver o captcha manualmente na
    janela do Chrome. Com o perfil persistente, isso só deve ser
    necessário de vez em quando (a sessão fica salva depois).
    """
    print('  🛑 Desafio do Cloudflare detectado ("Confirme que é humano").')
    print('     Resolva manualmente na janela do Chrome que está aberta.')
    try:
        input('     Depois de resolver, pressione ENTER aqui para continuar... ')
    except KeyboardInterrupt:
        print('     Cancelado pelo usuário.')
        raise
    sleep(2)


def salvar_diagnostico(motivo):
    """
    Salva screenshot + HTML da página em data/ para inspeção manual.
    Chamada sempre que algo essencial falha, para você ver exatamente
    o que a página mostrou no momento (login pedido? captcha? layout
    diferente do esperado?) sem precisar rodar tudo de novo.
    """
    try:
        screenshot_path = os.path.join(data_path, 'debug_screenshot.png')
        html_path = os.path.join(data_path, 'debug_page.html')
        driver.save_screenshot(screenshot_path)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(driver.page_source)
        print(f'  🔍 Diagnóstico salvo ({motivo}):')
        print(f'     {screenshot_path}')
        print(f'     {html_path}')
        print(f'     URL atual: {driver.current_url}')
        print(f'     navigator.webdriver = {driver.execute_script("return navigator.webdriver")}')
    except Exception as e:
        print(f'  ⚠️ Não foi possível salvar diagnóstico: {e}')


def clicar_com_retry(xpath, descricao, tentativas=3):
    """
    Tenta clicar num elemento. Se o clique for interceptado por um popup,
    fecha o popup e tenta novamente.
    """
    for i in range(tentativas):
        try:
            elemento = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
            sleep(0.5)
            elemento.click()
            print(f'  {descricao}: OK')
            return True
        except ElementClickInterceptedException:
            print(f'  {descricao}: clique bloqueado por popup (tentativa {i+1}/{tentativas}), tentando fechar...')
            fechar_popups()
            sleep(1)
        except TimeoutException:
            print(f'  {descricao}: elemento não encontrado (tentativa {i+1}/{tentativas})')
            sleep(1)

    # Fallback: clicar via JavaScript
    # ATENÇÃO: um clique via JS "funciona" sem lançar erro mesmo que o
    # elemento nunca fique de fato clicável/visível — por isso não é
    # garantia de que a ação real (ex.: download) aconteceu. Sempre
    # confirme o efeito esperado (arquivo baixado, popup fechado etc.)
    # depois de cair nesse fallback.
    try:
        elemento = driver.find_element(By.XPATH, xpath)
        driver.execute_script("arguments[0].click();", elemento)
        print(f'  {descricao}: OK (via JavaScript — clique não confirmado como real, valide o efeito)')
        return True
    except Exception as e:
        print(f'  {descricao}: FALHOU — {e}')
        salvar_diagnostico(f'falha ao clicar em "{descricao}"')
        return False


# --- Fluxo principal ---

# 1. Fechar popup inicial (se houver)
print('====== Verificando popups iniciais')
fechar_popups()

# 2. Executar busca
print('====== Busca')
path_busca = '//div/button[contains(@class,"find")]'
clicar_com_retry(path_busca, 'Botão Buscar')
sleep(3)

# 3. Fechar popup que pode aparecer após a busca
# Tenta algumas vezes com pequena espera entre elas — o popup promocional
# pode renderizar com atraso em relação aos resultados da busca.
print('====== Verificando popups pós-busca')
for _ in range(3):
    if fechar_popups():
        break
    sleep(1.5)

# 4. Download
print('====== Download')


def aguardar_arquivo_novo(arquivos_antes, timeout=20):
    """
    Espera até `timeout` segundos por um .csv novo em data_path que não
    existia antes do clique. Ignora arquivos .crdownload (download em
    andamento). Retorna o nome do arquivo novo, ou None se não apareceu
    nenhum — sinal de que o clique não disparou o download de verdade,
    mesmo que o Selenium não tenha lançado erro nenhum.
    """
    tentativas = int(timeout / 0.5)
    for _ in range(tentativas):
        atuais = set(os.listdir(data_path))
        novos = [f for f in (atuais - arquivos_antes) if f.endswith('.csv')]
        if novos:
            return novos[0]
        sleep(0.5)
    return None


arquivos_antes_download = set(os.listdir(data_path))

# Seletor por classe (o botão em si está correto — ele navega pra URL certa
# de exportação mesmo via clique JS; o problema real é o Cloudflare naquela
# URL, não o seletor)
path_download_classe = '//a[contains(@class,"btn-download")]'
path_download_absoluto = '//*[@id="main-2"]/div[4]/div/div[1]/div[2]/a'

clicar_com_retry(path_download_classe, 'Botão Download')
sleep(2)  # dá tempo da navegação/redirect do Cloudflare acontecer

if pagina_e_desafio_cloudflare():
    aguardar_resolucao_manual_cloudflare()

arquivo_baixado = aguardar_arquivo_novo(arquivos_antes_download)

if not arquivo_baixado:
    print('  Nenhum arquivo novo apareceu em data/ — o clique não confirmou o download.')
    print('  Tentando XPath alternativo (absoluto)...')
    salvar_diagnostico('nenhum arquivo novo após 1ª tentativa de download')
    clicar_com_retry(path_download_absoluto, 'Botão Download (XPath absoluto)')
    sleep(2)
    if pagina_e_desafio_cloudflare():
        aguardar_resolucao_manual_cloudflare()
    arquivo_baixado = aguardar_arquivo_novo(arquivos_antes_download)

if arquivo_baixado:
    print(f'  ✅ Download confirmado: {arquivo_baixado}')
else:
    print('  ⚠️ Download não confirmado após as duas tentativas.')
    salvar_diagnostico('nenhum arquivo novo após 2ª tentativa de download')

driver.quit()

# --- Renomear arquivo baixado ---
today = date.today().strftime('%d/%m/%Y')

for filename in os.listdir(data_path):
    if 'SI_Acoes' in filename:
        os.remove(os.path.join(data_path, filename))

arquivo_origem = os.path.join(data_path, 'statusinvest-busca-avancada.csv')
arquivo_destino = os.path.join(data_path, 'SI_Acoes.csv')

if os.path.exists(arquivo_origem):
    os.rename(arquivo_origem, arquivo_destino)
    print(f'====== Arquivo salvo em: {arquivo_destino}')
else:
    print('====== ATENÇÃO: arquivo CSV não encontrado em data/. Verifique se o download foi concluído.')
    print('====== Veja data/debug_screenshot.png e data/debug_page.html (se foram gerados)')
    print('====== para identificar a causa: pedido de login, captcha, ou layout mudado.')


# ---  Fundamentus 
 

import requests
import pandas as pd
from io import StringIO

url1 = 'https://www.fundamentus.com.br/resultado.php'
header = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"
}
r1 = requests.get(url1, headers=header)
dfs = pd.read_html(StringIO(r1.text), decimal=',', thousands='.')[0]

dfs.to_csv("data/fundamentuspp.csv", sep=';', encoding='utf-8', index=False)
