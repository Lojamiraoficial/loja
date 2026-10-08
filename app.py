import os
from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
app = Flask(__name__)

# IA MIRA
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash")
else:
    model = None

WHATSAPP = "5575987040465"

produtos = [
    {"id":1,"nome":"Fone Bluetooth P9 Pro Max","preco":89.90,"preco_antigo":199.90,"img":"https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=500","vendidos":"2.3k","desc":"Fone com cancelamento de ruído, bateria 40h, Bluetooth 5.3","cat":"eletronicos fone audio"},
    {"id":2,"nome":"Relógio Smartwatch T900 Pro","preco":129.90,"preco_antigo":299.90,"img":"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500","vendidos":"5.1k","desc":"Ligações, mede batimentos, IP67, bateria 7 dias","cat":"eletronicos relogio smartwatch"},
    {"id":3,"nome":"Kit 3 Camisas Oversized Premium","preco":99.90,"preco_antigo":189.90,"img":"https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500","vendidos":"8.9k","desc":"100% algodão, malha grossa, streetwear","cat":"moda camisa roupa oversized"},
    {"id":4,"nome":"Mini Projetor 4K Hy300 Portátil","preco":349.90,"preco_antigo":799.90,"img":"https://images.unsplash.com/photo-1593359677879-a4bb92f367d8?w=500","vendidos":"1.2k","desc":"Android 11, WiFi 6, 4K, 200 polegadas","cat":"eletronicos projetor casa cinema"},
    {"id":5,"nome":"Garrafa Térmica Stanley 1.2L","preco":79.90,"preco_antigo":149.90,"img":"https://images.unsplash.com/photo-1523369364227-249b4fdd7f08?w=500","vendidos":"12k","desc":"Mantém gelado 24h e quente 12h, original","cat":"casa garrafa termica stanley"},
    {"id":6,"nome":"Teclado Gamer RGB Mecânico","preco":159.90,"preco_antigo":329.90,"img":"https://images.unsplash.com/photo-1589578228447-e1a4e481c6c8?w=500","vendidos":"3.4k","desc":"Switch blue, ABNT2, LED RGB","cat":"games teclado gamer pc"},
    {"id":7,"nome":"Mouse Gamer Logitech G403","preco":199.90,"preco_antigo":399.90,"img":"https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=500","vendidos":"4.1k","desc":"16000 DPI, RGB, 6 botões programáveis","cat":"games mouse gamer"},
    {"id":8,"nome":"Caixa de Som JBL Boombox 3","preco":1299.00,"preco_antigo":2399.00,"img":"https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500","vendidos":"890","desc":"Bateria 24h, à prova d'água, 80W","cat":"eletronicos caixa som jbl boombox"},
    {"id":9,"nome":"Echo Dot 5ª Geração Alexa","preco":249.90,"preco_antigo":399.90,"img":"https://images.unsplash.com/photo-1589003077984-894e133dabab?w=500","vendidos":"9.5k","desc":"Alexa com som premium, controle casa inteligente","cat":"eletronicos alexa echo casa inteligente"},
    {"id":10,"nome":"AirPods Pro 2ª Geração","preco":899.90,"preco_antigo":1899.90,"img":"https://images.unsplash.com/photo-1600294037681-c80b4cb5b434?w=500","vendidos":"2.1k","desc":"Cancelamento ativo de ruído, bateria 30h","cat":"eletronicos fone airpods apple"},
    {"id":11,"nome":"Cadeira Gamer ThunderX3","preco":699.90,"preco_antigo":1299.90,"img":"https://images.unsplash.com/photo-1592078615290-033ee584e267?w=500","vendidos":"560","desc":"Ergonômica, reclinável 180°, almofadas","cat":"games cadeira gamer escritorio"},
    {"id":12,"nome":"Smart TV 50 Polegadas 4K QLED","preco":1899.00,"preco_antigo":2899.00,"img":"https://images.unsplash.com/photo-1593359677879-a4bb92f367d8?w=500","vendidos":"430","desc":"Google TV, Dolby Atmos, 60Hz","cat":"eletronicos tv smart 4k"},
    {"id":13,"nome":"Notebook Gamer Acer Nitro 5","preco":3299.00,"preco_antigo":4999.00,"img":"https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500","vendidos":"210","desc":"i5 12ª, RTX 3050, 8GB RAM, 512GB SSD","cat":"eletronicos notebook gamer pc"},
    {"id":14,"nome":"iPhone 15 Pro Max 256GB","preco":6899.00,"preco_antigo":9299.00,"img":"https://images.unsplash.com/photo-1592750475338-74b7b21085ab?w=500","vendidos":"1.8k","desc":"Titânio, câmera 120mm, A17 Pro","cat":"eletronicos iphone apple celular"},
    {"id":15,"nome":"Kit 5 Meias Esportivas","preco":39.90,"preco_antigo":79.90,"img":"https://images.unsplash.com/photo-1586350977771-b42a6d53c960?w=500","vendidos":"15k","desc":"Algodão, cano alto, antichulé","cat":"moda meia kit roupa"},
    {"id":16,"nome":"Mochila Executiva para Notebook","preco":89.90,"preco_antigo":169.90,"img":"https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500","vendidos":"3.2k","desc":"À prova d'água, USB, cabe 17 polegadas","cat":"moda mochila bolsa"},
    {"id":17,"nome":"Carregador Turbo 65W GaN","preco":69.90,"preco_antigo":129.90,"img":"https://images.unsplash.com/photo-1583394838336-acd977736f90?w=500","vendidos":"6.7k","desc":"3 portas, iPhone, Samsung, Notebook","cat":"eletronicos carregador turbo"},
    {"id":18,"nome":"Webcam Full HD 1080p com Microfone","preco":119.90,"preco_antigo":249.90,"img":"https://images.unsplash.com/photo-1587825140708-dfaf72ae4b04?w=500","vendidos":"1.9k","desc":"Autofoco, correção de luz, plug and play","cat":"eletronicos webcam pc"},
    {"id":19,"nome":"Controle PS5 DualSense Original","preco":399.90,"preco_antigo":549.90,"img":"https://images.unsplash.com/photo-1606144042614-b2417e99c4e3?w=500","vendidos":"2.8k","desc":"Original Sony, feedback háptico, gatilhos adaptáveis","cat":"games controle ps5 playstation"},
    {"id":20,"nome":"Tapete Gamer Grande 80x40 RGB","preco":59.90,"preco_antigo":119.90,"img":"https://images.unsplash.com/photo-1614294149010-950b698f72c0?w=500","vendidos":"4.5k","desc":"Borda costurada, base emborrachada, 14 modos RGB","cat":"games tapete mouse gamer"},
    {"id":21,"nome":"Suporte Articulado para Celular","preco":29.90,"preco_antigo":59.90,"img":"https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500","vendidos":"11k","desc":"Mesa, gravação, TikTok, regulável","cat":"eletronicos suporte celular"},
    {"id":22,"nome":"Luminária de Mesa LED Touch","preco":49.90,"preco_antigo":99.90,"img":"https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500","vendidos":"2.2k","desc":"3 cores, dimmer, USB, recarregável","cat":"casa luminaria led escritorio"},
    {"id":23,"nome":"Fone Gamer Havit RGB com Microfone","preco":79.90,"preco_antigo":159.90,"img":"https://images.unsplash.com/photo-1599669454699-248893623440?w=500","vendidos":"3.9k","desc":"P2 e USB, luz RGB, grave potente","cat":"games fone gamer headset"},
    {"id":24,"nome":"Power Bank 20000mAh Turbo","preco":89.90,"preco_antigo":179.90,"img":"https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=500","vendidos":"7.3k","desc":"Carrega 4 celulares, carga rápida 22.5W","cat":"eletronicos powerbank bateria"},
]

@app.route("/")
def home():
    return render_template("index.html", produtos=produtos, whatsapp=WHATSAPP)

@app.route("/produto/<int:id>")
def produto(id):
    p = next((x for x in produtos if x["id"] == id), None)
    return render_template("produto.html", p=p, whatsapp=WHATSAPP)

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message","")
    lista = "\n".join([f"- {p['nome']} R$ {p['preco']} ({p['cat']})" for p in produtos])
    prompt = f"""Você é a MIRA, vendedora da LOJA MIRA, super tecnológica, jovem e prestativa.
Produtos disponíveis:
{lista}
Cliente: {msg}
Responda curto, vendendo, e se perguntarem de produto cite nome e preço. Se for sobre frete diga que é grátis.
"""
    try:
        if model:
            resp = model.generate_content(prompt)
            return jsonify({"reply": resp.text})
        else:
            # busca simples sem IA
            achados = [p for p in produtos if any(k in p["cat"] for k in msg.lower().split())]
            if achados:
                return jsonify({"reply": f"Achei pra você: {achados[0]['nome']} por R$ {achados[0]['preco']} com frete grátis! Quer ver?"})
            return jsonify({"reply": "Me fala o que você procura? Tipo 'fone', 'gamer', 'iphone' que eu acho na hora!"})
    except Exception as e:
        return jsonify({"reply": "To com instabilidade mas me diz o que procura que eu acho! Ex: fone, tv, gamer"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)