// script.js - código compartilhado por todas as páginas do GameHub.

// Endereço base da API Flask. Se a API mudar de endereço, altere SOMENTE esta linha.
const API_URL = "http://127.0.0.1:5000/api";

// ---------- Menu do celular ----------
const botaoMenu = document.querySelector("#btn-menu");
if (botaoMenu) {
  botaoMenu.addEventListener("click", function () {
    document.querySelector("#menu").classList.toggle("aberto");
  });
}

// ---------- Mensagens de sucesso, erro e carregamento ----------
// tipo: "info", "sucesso" ou "erro" (as classes estão no CSS)
function mostrarMensagem(texto, tipo) {
  const caixa = document.querySelector("#mensagem");
  caixa.textContent = texto;
  caixa.classList.remove("info", "sucesso", "erro");
  caixa.classList.add(tipo);
}

function limparMensagem() {
  const caixa = document.querySelector("#mensagem");
  caixa.textContent = "";
  caixa.classList.remove("info", "sucesso", "erro");
}

// ---------- Card de jogo (usado no início e no catálogo) ----------
// pastaImg: caminho até img/jogos/ a partir da página atual
// paginaDetalhes: caminho até detalhes.html a partir da página atual
function criarCardJogo(jogo, pastaImg, paginaDetalhes) {
  const card = document.createElement("article");
  card.classList.add("card");

  const imagem = document.createElement("img");
  imagem.setAttribute("src", pastaImg + jogo.imagem);
  imagem.setAttribute("alt", "Capa de " + jogo.titulo);

  const corpo = document.createElement("div");
  corpo.classList.add("card-corpo");

  const titulo = document.createElement("h3");
  titulo.textContent = jogo.titulo;

  const info = document.createElement("p");
  info.textContent = jogo.desenvolvedora + " - " + jogo.ano_lancamento;

  const link = document.createElement("a");
  link.classList.add("botao", "botao-pequeno");
  link.setAttribute("href", paginaDetalhes + "?id=" + jogo.id);
  link.textContent = "Ver detalhes";

  corpo.appendChild(titulo);
  corpo.appendChild(info);
  corpo.appendChild(link);
  card.appendChild(imagem);
  card.appendChild(corpo);
  return card;
}

// ---------- Destaques da página inicial ----------
async function carregarDestaques() {
  const area = document.querySelector("#destaques");
  mostrarMensagem("Carregando jogos...", "info");
  try {
    const resposta = await fetch(API_URL + "/jogos");
    const jogos = await resposta.json();
    if (jogos.erro) {
      mostrarMensagem(jogos.erro, "erro");
      return;
    }
    area.innerHTML = "";
    for (let i = 0; i < jogos.length && i < 4; i++) {
      area.appendChild(criarCardJogo(jogos[i], "img/jogos/", "pages/detalhes.html"));
    }
    limparMensagem();
  } catch (erro) {
    mostrarMensagem("Não foi possível conectar à API. Verifique se o Flask está rodando.", "erro");
  }
}

// Só roda na página inicial (a única que tem #destaques)
if (document.querySelector("#destaques")) {
  carregarDestaques();
}
